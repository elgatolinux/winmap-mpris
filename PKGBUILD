# Maintainer: el gato <gato.mega.mp3@gmail.com>
pkgname=winamp-mpris
pkgver=0.1.1
pkgrel=1
pkgdesc="MPRIS bridge for Winamp running under Wine (exposes a playerctl-compatible MPRIS endpoint)"
arch=('any')
url="https://github.com/elgatolinux/winamp-mpris"
license=('MIT')
depends=('python' 'wine' 'playerctl' 'python-dbus-next')
provides=('winamp-mpris')
conflicts=()
replaces=()
source=(
  "winamp-mpris.py"
  "winamp-mpris.service"
  "clamp.exe::https://winampheritage.com/plugin/144432/CLAmp.exe"
)

sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP')

prepare() {
  cd "$srcdir"

}

package() {
  cd "$srcdir"

  install -Dm755 winamp-mpris.py "$pkgdir/usr/bin/winamp-mpris"

  install -Dm644 winamp-mpris.service "$pkgdir/usr/lib/systemd/user/winamp-mpris.service"
  # Install clamp.exe to a read-only system location so Wine can reference it via Z: drive
  install -Dm644 clamp.exe "$pkgdir/usr/share/winamp-mpris/clamp.exe"



}

