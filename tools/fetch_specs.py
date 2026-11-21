"""Fetch the public Material site content and resolve its published token tables.

Python standard library only. Run from any directory; outputs are repository relative.
"""
import concurrent.futures
import hashlib
import gzip
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://m3.material.io"


def fetch(path):
    with urllib.request.urlopen(BASE + path, timeout=120) as response:
        return response.read()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == '.gz':
        path.write_bytes(gzip.compress(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    else:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    html = fetch('/components').decode()
    script = re.search(r'src="([^"]*/main\.[^"]+\.js)"', html)[1]
    js = fetch(script).decode()
    version = re.search(r'carbonVersion:"([^"]+)"', js)[1]
    routes = re.findall(r'"slug":"(components/[^" ]+)","exportedCarbonFileId":"([^"]+)"', js)
    manifest = {'version': version, 'script': BASE + script, 'pages': []}

    def page(route):
        slug, file_id = route
        url = f'/_dsm/content/m3/{version}/{file_id}'
        data = json.loads(fetch(url))
        sections = [s for s in data['sections'] if s['name'] == 'Specs' and s.get('isVisible', True)]
        chunks = [c for s in sections for b in s['contentBlocks'] if not b.get('isHidden') for c in b['contentChunks']]
        tables = sorted({c['resourceName'].split('/')[-1] for c in chunks if c.get('libraryModuleType') == 'TOKEN_TABLE'})
        # Preserve specs text, diagram URLs, and table configuration without editorial metadata.
        content = [{k: c[k] for k in ['htmlValue', 'footer', 'altText', 'imageUrl', 'resourceName', 'libraryModuleType', 'moduleConfigurationOverrides'] if c.get(k)} for c in chunks]
        save(ROOT / 'specs/pages' / (slug.split('/')[-1] + '.json'), content)
        return {'slug': slug, 'title': data['title'], 'url': BASE + '/' + slug + '/specs', 'dataUrl': BASE + url, 'tables': tables, 'hasSpecs': bool(sections)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        manifest['pages'] = sorted(pool.map(page, routes), key=lambda p: p['slug'])
    table_ids = sorted({t for p in manifest['pages'] for t in p['tables']})

    def table(table_id):
        url = f'/_dsm/data/dsdb-m3/{version}/TOKEN_TABLE.{table_id}.json'
        raw = fetch(url)
        system = json.loads(raw)['system']
        tags = {t['name']: t['displayName'] for t in system['tags']}
        sets = {s['name']: s for s in system['tokenSets']}
        normalized = {'url': BASE + url, 'sha256': hashlib.sha256(raw).hexdigest(), 'version': system['dsdbVersion'], 'sets': []}
        for name, token_set in sets.items():
            tokens = []
            for token in system['tokens']:
                if not token['name'].startswith(name + '/tokens/'):
                    continue
                variants = []
                for v in system['contextualReferenceTrees'].get(token['name'], {}).get('contextualReferenceTree', []):
                    variants.append({'contexts': sorted(tags[t] for t in v.get('contextTags', [])), 'value': v.get('resolvedValue'), 'references': references(v.get('referenceTree', {}))})
                raw_values = [{k: v for k, v in value.items() if k not in ['name', 'revisionId', 'revisionCreateTime', 'state', 'createTime']} for value in system['values'] if value['name'].startswith(token['name'] + '/values/')]
                tokens.append({'name': token['tokenName'], 'suffix': token.get('tokenNameSuffix'), 'displayName': token.get('displayName', ''), 'type': token.get('tokenValueType'), 'deprecated': token.get('deprecationMessage', {}).get('message'), 'variants': variants, 'rawValues': raw_values})
            normalized['sets'].append({'name': token_set['tokenSetName'], 'displayName': token_set['displayName'], 'tokens': sorted(tokens, key=lambda t: t['name'])})
        save(ROOT / 'specs/tokens' / (table_id + '.json.gz'), normalized)
        return table_id

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(table, table_ids))
    system_url = f'/_dsm/data/dsdb-m3/{version}/TOKEN_TYPE_UNSPECIFIED.20543ce18892f7d9.json'
    system = json.loads(fetch(system_url))['system']
    save(ROOT / 'specs/motion.json', extract_motion(system, BASE + system_url))
    save(ROOT / 'specs/manifest.json', manifest)
    print(f"Fetched {len(routes)} pages and {len(table_ids)} token tables ({version}).")


def references(node):
    result = [node['tokenName']] if node.get('tokenName') else []
    for child in node.get('childNodes', []):
        result.extend(references(child))
    return list(dict.fromkeys(result))


def extract_motion(system, url):
    tags = {t['name']: t['displayName'] for t in system['tags']}
    result = {'url': url, 'tokens': []}
    for token in system['tokens']:
        if token.get('tokenName', '').startswith('md.sys.motion.spring.fast.spatial.'):
            variants = []
            for variant in system['contextualReferenceTrees'][token['name']]['contextualReferenceTree']:
                contexts = sorted(tags[t] for t in variant.get('contextTags', []))
                if 'Android' in contexts:
                    variants.append({'contexts': contexts, 'value': variant['resolvedValue']})
            result['tokens'].append({'name': token['tokenName'], 'variants': variants})
    return result


if __name__ == '__main__':
    main()
