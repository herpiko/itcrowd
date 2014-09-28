import os

def populate():
   Kathw.objects.get_or_create(kathw='PC')
   Kathw.objects.get_or_create(kathw='Laptop')
   Kathw.objects.get_or_create(kathw='Server')
   Kathw.objects.get_or_create(kathw='Printer')
   Kathw.objects.get_or_create(kathw='Jaringan')
   Kathw.objects.get_or_create(kathw='Perangkat lunak')


   Lokasi.objects.get_or_create(lokasi='Mataram')
   Lokasi.objects.get_or_create(lokasi='Lembar')
   Lokasi.objects.get_or_create(lokasi='BIL')
   Lokasi.objects.get_or_create(lokasi='LabKH')
   Lokasi.objects.get_or_create(lokasi='LabKT')
   Lokasi.objects.get_or_create(lokasi='Kayangan')
   Lokasi.objects.get_or_create(lokasi='Pemenang')

   User.objects.get_or_create(username='piko', email='herpiko@gmail.com',first_name='Herpiko Dwi Aguno', is_staff=True)
   User.objects.get_or_create(username='dian', email='dians1ti@gmail.com',first_name='Dian Alfasaris', is_staff=True)
   User.objects.get_or_create(username='umum', email='bkp_mataram@yahoo.co.id',first_name='Umum', is_staff=False)
   

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_maintenance.settings')
    from main.models import Lokasi, User, Kathw
    populate()
