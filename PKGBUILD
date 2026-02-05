pkgname=winamp-mpris
pkgver=0.1.0
pkgrel=1
pkgdesc="MPRIS bridge for Winamp running under Wine"
arch=('any')
url="https://github.com/elgatolinux/winamp-mpris"
license=('MIT')
depends=('python' 'wine' 'playerctl' 'python-dbus-next' 'wmctrl')
source=(
  "winamp-mpris.py"
  "winamp-mpris.service"
  "winamp-title.sh"
)
sha256sums=('SKIP' 'SKIP' 'SKIP')

package() {
  install -Dm755 winamp-mpris.py "$pkgdir/usr/bin/winamp-mpris"
  install -Dm644 winamp-mpris.service "$pkgdir/usr/lib/systemd/user/winamp-mpris.service"
  install -Dm755 winamp-title.sh "$pkgdir/usr/bin/winamp-title"
}
