import os

def tgl2db(tgl):
  glue=''
  sec = (tgl[6:],tgl[3:5],tgl[:2])
  tgl = glue.join(sec)
  return tgl

def repair():
   tindakan = Tindakan.objects.all()
   for x in tindakan:
      x.tanggal_buka = tgl2db(x.tanggal_buka)
      x.tanggal_tutup = tgl2db(x.tanggal_tutup) 
      item = Tindakan.objects.filter(noid_tin=x.noid_tin).get()
      item.tanggal_buka = x.tanggal_buka
      item.tanggal_tutup = x.tanggal_tutup
      item.save()

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_maintenance.settings')
    from main.models import Tindakan
    repair()
