import unittest
from launcher import command


class LauncherTests(unittest.TestCase):
    env = {"WALLET": "prl1p" + "q" * 58, "SALAD_MACHINE_ID": "same-node"}

    def test_replicas_and_same_machine_groups_do_not_collide(self):
        names = [command(self.env)[8] for _ in range(10000)]
        self.assertEqual(len(set(names)), 10000)
        self.assertTrue(all(name.startswith("salad-") for name in names))

    def test_pool_and_wallet(self):
        cmd = command(self.env)
        self.assertEqual(cmd[4], "pool.pearlhash.xyz:9000")
        self.assertEqual(cmd[6], self.env["WALLET"])

    def test_invalid_wallet_and_prefix(self):
        for env in ({}, {"WALLET": "https://pearlhash.xyz/account/test"},
                    dict(self.env, WORKER_PREFIX="bad.name")):
            with self.assertRaises(ValueError):
                command(env)


if __name__ == "__main__":
    unittest.main()
