# zipalign 대용: 압축하지 않은 항목을 4바이트 경계에 맞춘다.
import sys, zipfile, struct
src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
with open(dst, 'wb') as f:
    zout = zipfile.ZipFile(f, 'w')
    for info in zin.infolist():
        data = zin.read(info.filename)
        ni = zipfile.ZipInfo(info.filename, date_time=(1981, 1, 1, 1, 1, 2))
        ni.external_attr = info.external_attr
        ni.create_system = 0
        stored = info.compress_type == zipfile.ZIP_STORED or info.filename == 'resources.arsc'
        ni.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
        ni.extra = b''
        if stored:
            off = f.tell() + 30 + len(ni.filename.encode('utf-8'))
            pad = (4 - off % 4) % 4
            if pad:
                # 0xD935 = Android zipalign extra field; minimum 4-byte header, so pad to 4..7
                n = pad if pad >= 4 else pad + 4
                ni.extra = struct.pack('<HH', 0xD935, n - 4) + b'\0' * (n - 4) if n >= 4 else b''
                # recompute: extra length n must make offset aligned
                assert (off + n) % 4 == 0
        zout.writestr(ni, data)
    zout.close()
