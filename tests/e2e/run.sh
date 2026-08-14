#!/bin/sh
set -eu

fail() {
    echo "FAIL: $1" >&2
    exit 1
}

BALANCER="$(command -v btrfs-auto-balancer)" || fail "btrfs-auto-balancer is not on PATH after install"
echo "ok: btrfs-auto-balancer installed at ${BALANCER}"

command -v btrfsauba >/dev/null || fail "the btrfsauba alias is not on PATH after install"
echo "ok: btrfsauba alias installed"

case "${BALANCER}" in
    /usr/local/bin/*) ;;
    *) fail "btrfs-auto-balancer resolved to ${BALANCER}, outside the install prefix" ;;
esac
echo "ok: resolved from the installed package, not the source tree"

command -v findmnt >/dev/null || fail "findmnt is missing from the image"
command -v btrfs >/dev/null || fail "btrfs is missing from the image"
echo "ok: real findmnt and btrfs present"

btrfs-auto-balancer --help | grep -q "btrfs balance" || fail "--help does not describe the tool"
echo "ok: --help"

set +e
output="$(btrfs-auto-balancer 90 0 2>&1)"
status=$?
set -e
[ "${status}" -eq 2 ] || fail "a zero step exited ${status}, expected 2"
echo "${output}" | grep -q "must be greater than zero" || fail "zero step message wrong"
echo "ok: a zero countdown step is rejected with exit 2"

set +e
output="$(btrfs-auto-balancer 90 2>&1)"
status=$?
set -e
[ "${status}" -eq 2 ] || fail "a missing argument exited ${status}, expected 2"
echo "ok: a missing argument exits 2"

set +e
output="$(btrfs-auto-balancer 90 10 2>&1)"
status=$?
set -e
[ "${status}" -eq 1 ] || fail "a container without btrfs mounts exited ${status}, expected 1"
echo "${output}" | grep -q "No Btrfs filesystems found." || fail "empty findmnt result not reported"
echo "ok: real findmnt finds no btrfs mount, exits 1"

set +e
output="$(env PATH=/nonexistent-bin "${BALANCER}" 90 10 2>&1)"
status=$?
set -e
[ "${status}" -eq 127 ] || fail "missing findmnt exited ${status}, expected 127"
echo "${output}" | grep -q "required command 'findmnt' is not installed" || fail "missing findmnt message wrong"
if echo "${output}" | grep -q "Traceback"; then
    fail "missing findmnt produced a traceback"
fi
echo "ok: missing findmnt exits 127 with a clean message"

set +e
output="$(env PATH=/nonexistent-bin "${BALANCER}" 90 10 --drive_path /data 2>&1)"
status=$?
set -e
[ "${status}" -eq 127 ] || fail "missing btrfs exited ${status}, expected 127"
echo "${output}" | grep -q "required command 'btrfs' is not installed" || fail "missing btrfs message wrong"
echo "ok: missing btrfs exits 127 with a clean message"

# A real btrfs filesystem on a loop device. Needs --privileged, which is why the
# make target passes it. mount -o loop sets AUTOCLEAR, so umount frees the device.
truncate -s 400M /tmp/btrfs.img
mkfs.btrfs -q /tmp/btrfs.img || fail "mkfs.btrfs failed"
mkdir -p /mnt/btrfs
set +e
mount_error="$(mount -o loop /tmp/btrfs.img /mnt/btrfs 2>&1)"
mount_status=$?
set -e
[ "${mount_status}" -eq 0 ] || fail "could not mount the loop filesystem: ${mount_error}"
echo "ok: real btrfs filesystem mounted at /mnt/btrfs"

findmnt -t btrfs -o TARGET --noheadings -n -r | grep -q "/mnt/btrfs" \
    || fail "findmnt does not report the new btrfs mount"
echo "ok: findmnt reports it"

set +e
output="$(btrfs-auto-balancer 20 5 --drive_path /mnt/btrfs 2>&1)"
status=$?
set -e
[ "${status}" -eq 0 ] || fail "balancing a real filesystem exited ${status}, expected 0"
echo "${output}" | grep -q -- "-dusage=20 -musage=20 /mnt/btrfs" || fail "the first pass is missing"
echo "${output}" | grep -q -- "-dusage=15 -musage=15 /mnt/btrfs" || fail "the second pass is missing"
echo "${output}" | grep -q -- "-dusage=10 -musage=10 /mnt/btrfs" || fail "the third pass is missing"
if echo "${output}" | grep -q -- "-dusage=5"; then
    fail "balancing continued at or below the minimum usage"
fi
echo "ok: real btrfs balance runs three passes at 20, 15 and 10 then stops"

set +e
output="$(btrfs-auto-balancer 20 15 2>&1)"
status=$?
set -e
[ "${status}" -eq 0 ] || fail "discovery mode exited ${status}, expected 0"
echo "${output}" | grep -q -- "-dusage=20 -musage=20 /mnt/btrfs" \
    || fail "the discovered mount was not balanced"
echo "ok: without --drive_path the mount is discovered through real findmnt and balanced"

umount /mnt/btrfs || fail "could not unmount the loop filesystem"
echo "ok: loop filesystem released"

echo "ALL E2E CHECKS PASSED"
