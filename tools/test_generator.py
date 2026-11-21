"""Contract tests for source coverage, units, contexts, and generated API integrity."""
import gzip
import json
import unittest

from generate_specs import ROOT, choose, expression, generate


def tokens():
    return {
        token['name']: token
        for path in (ROOT / 'specs/tokens').glob('*.json.gz')
        for token_set in json.loads(gzip.decompress(path.read_bytes()))['sets']
        for token in token_set['tokens']
    }


class GeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokens = tokens()

    def test_every_published_token_has_exactly_one_api_property(self):
        files, coverage = generate()
        index = json.loads(files[ROOT / 'specs/api-index.json'])
        self.assertEqual(set(self.tokens), {entry['token'] for entry in index})
        self.assertEqual(len(self.tokens), len(index))
        self.assertEqual(len(index), len({entry['property'] for entry in index}))
        self.assertEqual(37, coverage['specPages'])

    def test_static_third_party_typography_does_not_pick_google_sans_or_ios_bold(self):
        token = self.tokens['md.comp.app-bar.medium-flexible.title.font']
        style = choose(token)['value']['type']
        self.assertEqual(['Roboto'], style['fontNames']['values'])
        self.assertEqual(400, style['fontWeight'])
        self.assertEqual(28, style['fontSize']['value'])
        self.assertEqual(36, style['lineHeight']['value'])

    def test_theme_color_roles_are_preserved(self):
        token = self.tokens['md.comp.app-bar.container.color']
        self.assertEqual(('Color', 'MaterialTheme.colorScheme.surface', True), expression(token))

    def test_percentages_are_not_misinterpreted_as_dp(self):
        token = self.tokens['md.comp.sheet.side.docked.container.height']
        self.assertEqual(('Float', '1f', False), expression(token))

    def test_zero_dimension_is_a_real_value(self):
        token = self.tokens['md.comp.app-bar.icon-button-space']
        self.assertEqual(('Dp', '0.dp', False), expression(token))

    def test_flexible_app_bar_height_distinguishes_subtitle(self):
        self.assertEqual('120.dp', expression(self.tokens['md.comp.app-bar.large-flexible.container.height'])[1])
        self.assertEqual('152.dp', expression(self.tokens['md.comp.app-bar.large-flexible.with-subtitle.container.height'])[1])

    def test_motion_composite_matches_system_source(self):
        source = json.loads((ROOT / 'specs/motion.json').read_text(encoding='utf-8'))
        values = {t['name']: next(v['value']['numeric'] for v in t['variants'] if 'Standard' in v['contexts']) for t in source['tokens']}
        self.assertEqual(0.9, values['md.sys.motion.spring.fast.spatial.damping'])
        self.assertEqual(1400, values['md.sys.motion.spring.fast.spatial.stiffness'])


if __name__ == '__main__':
    unittest.main()
