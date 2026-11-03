#!/usr/bin/env python3
"""Build the audit_tree for the Linux permissions audit lab.

Creates a small fake filesystem tree with a deliberate mix of healthy
and broken permissions: two setuid binaries (one of them a forgotten
test shell), a world-writable upload directory, a world-readable
private key backup, and a world-readable shadow backup that holds
the lab flag. Run it, then audit the tree you just made.
"""
import os
import stat

ROOT = "audit_tree"

def write(path, content, mode):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(content)
    os.chmod(full, mode)

def main():
    write("bin/report_gen", "#!/bin/sh\necho quarterly report\n", 0o755)
    write("bin/backup_tool", "#!/bin/sh\necho backup running\n", 0o4755)
    write("bin/testshell", "#!/bin/sh\necho leftover test shell, still setuid\n", 0o4755)
    write("etc/app.conf", "listen = 8080\ndebug = false\n", 0o644)
    write("etc/passwd.bak", "root:x:0:0:root:/root:/bin/bash\n", 0o600)
    write("etc/shadow.bak",
          "root:$6$rounds=5000$saltsalt$9JZ7ExampleHashOnlyNotARealCredential:19600:0:99999:7:::\n"
          "flag: SALVO{suid_audit_shadow_bak_world_readable}\n", 0o644)
    write("home/user/.ssh/id_rsa.bak",
          "-----BEGIN OPENSSH PRIVATE KEY-----\n"
          "b3BlbnNzaC1rZXktdjEAAAAA-example-not-a-real-key\n"
          "-----END OPENSSH PRIVATE KEY-----\n", 0o644)
    write("home/user/notes.txt", "patch window is thursday\n", 0o644)
    write("var/www/html/index.html", "<h1>portal</h1>\n", 0o644)
    upload = os.path.join(ROOT, "var/www/upload")
    os.makedirs(upload, exist_ok=True)
    os.chmod(upload, 0o777)
    print("audit_tree built")

if __name__ == "__main__":
    main()
