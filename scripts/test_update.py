import unittest

from update import formula


class FormulaTest(unittest.TestCase):
    def setUp(self):
        self.assets = [
            {"name": f"pgram_0.1.0_{os}_{arch}.tar.gz", "browser_download_url":
             f"https://github.com/lucasheriques/pgram/releases/download/v0.1.0/pgram_0.1.0_{os}_{arch}.tar.gz"}
            for os in ("darwin", "linux") for arch in ("arm64", "amd64")
        ]
        self.release = {"tag_name": "v0.1.0", "assets": self.assets}
        self.checksums = "\n".join("a" * 64 + "  " + asset["name"] for asset in self.assets)

    def test_maps_all_platforms_to_verified_checksums(self):
        result = formula(self.release, self.checksums)
        self.assertEqual(result.count("sha256"), 4)
        for asset in self.assets:
            self.assertIn(asset["browser_download_url"], result)

    def test_rejects_unexpected_release_data(self):
        for case in ("tag", "url", "checksum", "missing"):
            with self.subTest(case=case):
                self.setUp()
                if case == "tag":
                    self.release["tag_name"] = 'v0.1.0"'
                elif case == "url":
                    self.assets[0]["browser_download_url"] = "https://example.com/binary"
                elif case == "checksum":
                    self.checksums = self.checksums.replace("a" * 64, "invalid")
                else:
                    self.checksums = ""
                with self.assertRaises((ValueError, KeyError)):
                    formula(self.release, self.checksums)


if __name__ == "__main__":
    unittest.main()
