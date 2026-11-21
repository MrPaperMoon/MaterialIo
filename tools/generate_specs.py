"""Generate typed Compose constants from the checked-in Material token snapshot."""
import argparse
import gzip
import json
import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'material-specs/src/commonMain/kotlin/io/material/specs'
CONTEXT = {'3P', 'Android', 'Static', 'Light', 'Default', 'None', 'Standard', 'Mobile'}
IMPORTS = {
    'Composable': 'androidx.compose.runtime.Composable',
    'Dp': 'androidx.compose.ui.unit.Dp', 'dp': 'androidx.compose.ui.unit.dp',
    'TextUnit': 'androidx.compose.ui.unit.TextUnit', 'sp': 'androidx.compose.ui.unit.sp',
    'Color': 'androidx.compose.ui.graphics.Color',
    'MaterialTheme': 'androidx.compose.material3.MaterialTheme',
    'Shape': 'androidx.compose.ui.graphics.Shape',
    'RoundedCornerShape': 'androidx.compose.foundation.shape.RoundedCornerShape',
    'AbsoluteRoundedCornerShape': 'androidx.compose.foundation.shape.AbsoluteRoundedCornerShape',
    'TextStyle': 'androidx.compose.ui.text.TextStyle',
    'FontWeight': 'androidx.compose.ui.text.font.FontWeight',
    'FontFamily': 'androidx.compose.ui.text.font.FontFamily',
    'MaterialFonts': 'io.material.specs.styles.MaterialFonts',
    'MotionSpring': 'io.material.specs.styles.MotionSpring',
}


def camel(value, upper=False):
    words = re.findall(r'[A-Za-z0-9]+', value)
    result = ''.join(w[:1].upper() + w[1:] for w in words)
    if result[0].isdigit():
        result = 'Value' + result
    return result if upper else result[:1].lower() + result[1:]


def choose(token, dark=False):
    allowed = CONTEXT - {'Light'} | {'Dark'} if dark else CONTEXT
    variants = [v for v in token['variants'] if set(v['contexts']) <= allowed]
    if not variants:
        raise ValueError(f"No matching context: {token['name']}")
    return max(variants, key=lambda v: len(v['contexts']))


def number(value):
    return format(value, '.9g')


def literal_color(value):
    channels = [round(value.get(c, 1 if c == 'alpha' else 0) * 255) for c in ['alpha', 'red', 'green', 'blue']]
    return 'Color(0x' + ''.join(f'{c:02X}' for c in channels) + ')'


def expression(token):
    variant = choose(token)
    value = variant['value']
    if value is None:
        assert 'md.sys.motion.spring.fast.spatial' in variant['references']
        return 'MotionSpring', 'MotionSpring.fastSpatialStandard', False
    if 'color' in value:
        roles = [r.removeprefix('md.sys.color.') for r in variant['references'] if r.startswith('md.sys.color.')]
        if roles:
            role = roles[0]
            return 'Color', 'Color.Black' if role == 'shadow' else 'MaterialTheme.colorScheme.' + camel(role), role != 'shadow'
        dark = choose(token, dark=True)['value']['color']
        light_expr = literal_color(value['color'])
        dark_expr = literal_color(dark)
        if light_expr != dark_expr:
            return 'Color', f'if (androidx.compose.foundation.isSystemInDarkTheme()) {dark_expr} else {light_expr}', True
        return 'Color', light_expr, False
    for key in ['length', 'elevation', 'fontSize', 'lineHeight', 'fontTracking']:
        if key in value:
            unit = value[key].get('unit')
            if unit == 'PERCENT':
                return 'Float', number(value[key].get('value', 0) / 100) + 'f', False
            assert unit in ['DIPS', 'POINTS'], (token['name'], value)
            is_text = key in ['fontSize', 'lineHeight', 'fontTracking']
            return ('TextUnit' if is_text else 'Dp'), number(value[key].get('value', 0)) + ('.sp' if is_text else '.dp'), False
    for key in ['numeric', 'opacity']:
        if key in value:
            return 'Float', number(value[key]) + 'f', False
    if 'fontWeight' in value:
        return 'FontWeight', f"FontWeight({value['fontWeight']})", False
    if 'fontNames' in value:
        assert value['fontNames']['values'] == ['Roboto'], value
        return 'FontFamily', 'MaterialFonts.roboto', True
    if 'shape' in value:
        shape = value['shape']
        if shape['family'] == 'SHAPE_FAMILY_CIRCULAR':
            return 'Shape', 'RoundedCornerShape(percent = 50)', False
        assert shape['family'] == 'SHAPE_FAMILY_ROUNDED_CORNERS'
        size = shape.get('defaultSize', {}).get('value', 0)
        corners = ['topLeft', 'topRight', 'bottomRight', 'bottomLeft']
        if any(k in shape for k in corners):
            args = ', '.join(f'{k} = {number(shape.get(k, {}).get("value", 0) if k in shape else size)}.dp' for k in corners)
            return 'Shape', f'AbsoluteRoundedCornerShape({args})', False
        return 'Shape', f'RoundedCornerShape({number(size)}.dp)', False
    if 'type' in value:
        style = value['type']
        assert style['fontNames']['values'] == ['Roboto'], style
        args = ['fontFamily = MaterialFonts.roboto', f'fontWeight = FontWeight({style["fontWeight"]})']
        for key, name in [('fontSize', 'fontSize'), ('lineHeight', 'lineHeight'), ('fontTracking', 'letterSpacing')]:
            args.append(f'{name} = {number(style[key].get("value", 0))}.sp')
        return 'TextStyle', 'TextStyle(\n' + ''.join('            ' + a + ',\n' for a in args) + '        )', True
    raise ValueError((token['name'], value))


def class_name(token_set):
    name = camel(token_set['name'].removeprefix('md.comp.').removeprefix('md.'), True)
    if ' - Common' in token_set['displayName']:
        name += 'Common'
    return name


def generate():
    manifest = json.loads((ROOT / 'specs/manifest.json').read_text(encoding='utf-8'))
    pages = manifest['pages']
    # Shared search/button sets belong to their own component, not their referring page.
    pages = sorted(pages, key=lambda p: (p['slug'] not in ['components/search', 'components/buttons'], p['slug']))
    seen = {}
    files = {}
    index = []
    rows = []
    measurements = json.loads((ROOT / 'specs/measurement-overrides.json').read_text(encoding='utf-8'))
    measurement_count = 0
    for page in pages:
        package = page['slug'].split('/')[-1].replace('-', '_')
        page_objects = 0
        page_tokens = 0
        for table in page['tables']:
            data = json.loads(gzip.decompress((ROOT / 'specs/tokens' / (table + '.json.gz')).read_bytes()))
            for token_set in data['sets']:
                if token_set['name'] in seen:
                    assert seen[token_set['name']] == token_set, token_set['name']
                    continue
                seen[token_set['name']] = token_set
                page_objects += 1
                page_tokens += len(token_set['tokens'])
                name = class_name(token_set)
                body = [f'/**\n * {token_set["displayName"]}.\n *\n * [Material 3 specs]({page["url"]}).\n * Token set: `{token_set["name"]}`. Snapshot: {manifest["version"]}.\n */\nobject {name} {{']
                names = set()
                for token in token_set['tokens']:
                    prop = camel(token['suffix'] or token['name'].removeprefix(token_set['name'] + '.'))
                    assert prop not in names, (name, prop)
                    names.add(prop)
                    typ, expr, composable = expression(token)
                    doc = token['displayName'].replace('*/', '* /').replace('\n', ' ')
                    body.append('    /**')
                    body.extend('     * ' + line for line in textwrap.wrap(doc + '.', width=108))
                    body.append(f'     * Token: `{token["name"]}`.')
                    raw = choose(token)['value'] or {}
                    if raw.get('length', {}).get('unit') == 'PERCENT':
                        body.append('     * Percentage expressed as a fraction: 100% equals 1f.')
                    body.append('     */')
                    if token.get('deprecated'):
                        message = json.dumps(token['deprecated'], ensure_ascii=False).replace('$', '\\$')
                        body.append(f'    @Deprecated({message})')
                    if composable:
                        body.append(f'    val {prop}: {typ}\n        @Composable get() = {expr}')
                    else:
                        body.append(f'    val {prop}: {typ} = {expr}')
                    body.append('')
                    index.append({'token': token['name'], 'property': f'io.material.specs.{package}.{name}.{prop}', 'source': page['url']})
                extra = measurements.get(token_set['name'], {})
                for prop, value in extra.get('properties', {}).items():
                    assert prop not in names, (name, prop)
                    body.append('    /**')
                    body.append('     * Measurement transcribed from the specification diagram; no published token name.')
                    body.append(f'     * [Source]({extra["source"]}).')
                    body.append('     */')
                    body.append(f'    val {prop}: Dp = {number(value)}.dp\n')
                    measurement_count += 1
                body = '\n'.join(body).rstrip() + '\n}\n'
                imports = '\n'.join('import ' + path for symbol, path in sorted(IMPORTS.items(), key=lambda x: x[1]) if re.search(r'\b' + symbol + r'\b', body))
                path = OUTPUT / package / (name + '.kt')
                assert path not in files, path
                files[path] = f'// Generated by tools/generate_specs.py. Do not edit.\npackage io.material.specs.{package}\n\n{imports}\n\n{body}'
        rows.append(f'| [{page["title"]}]({page["url"]}) | `{package}` | {page_objects} | {page_tokens} |')
    files[ROOT / 'specs/api-index.json'] = json.dumps(index, ensure_ascii=False, indent=2) + '\n'
    assert set(measurements) <= set(seen)
    coverage = {'pages': len(pages), 'specPages': sum(p['hasSpecs'] for p in pages), 'objects': len(seen), 'tokenProperties': len(index), 'measurementProperties': measurement_count, 'properties': len(index) + measurement_count, 'context': sorted(CONTEXT)}
    files[ROOT / 'specs/coverage.json'] = json.dumps(coverage, indent=2) + '\n'
    files[ROOT / 'specs/COVERAGE.md'] = '\n'.join([
        '# Token coverage', '',
        f'Snapshot: `{manifest["version"]}`. All published table tokens have an API mapping.', '',
        'Shared token sets are counted once, under their owning component. See `api-index.json`.', '',
        '| Specs page | Kotlin package | Objects | Token properties |',
        '| --- | --- | ---: | ---: |',
        *sorted(rows), '',
        f'Total: {len(seen)} objects, {len(index)} token properties, {measurement_count} supplementary diagram measurements.', '',
        '## Diagram coverage', '',
        'The six App bar measurement diagrams have been visually reviewed. Additional measurements',
        'are in `measurement-overrides.json`. Other component diagrams are preserved as source URLs',
        'in `pages/*.json`; their numbers have not all been transcribed to Kotlin.', '',
        '## Context coverage', '',
        'The API uses 3P / Android / Static / Default, Standard motion, Mobile, None overlay.',
        'System colors resolve against the current Compose MaterialTheme. The snapshots retain all',
        'published contexts, but the API does not expose an automatic native-platform context switch.', '',
    ])
    return files, coverage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files, coverage = generate()
    stale = []
    for path, text in files.items():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8', newline='\n')
    generated = {p for p in OUTPUT.rglob('*.kt') if p.read_text(encoding='utf-8').startswith('// Generated by tools/generate_specs.py.')}
    stale.extend(str(p.relative_to(ROOT)) for p in generated - files.keys())
    if stale:
        raise SystemExit('Stale generated files: ' + ', '.join(stale))
    print(coverage)


if __name__ == '__main__':
    main()
