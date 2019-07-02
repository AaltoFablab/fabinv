from mongoengine import connect
from models import Created, Location, Item

connect(
    'fabinv', 
    host='127.0.0.1', 
    port=27017, 
    username='fabadmin', 
    password='thereisnofuture', 
    authentication_source='admin')

def init_db():
    # Check if we did this already
    if Created.objects(yes=True).count():
        return
    else:
        creation = Created()
        creation.save()

    # Locations
    storage = Location(name='Storage Room')
    storage.save()

    assembly = Location(name='Assembly Room')
    assembly.save()

    electronics = Location(name='Electronics')
    electronics.save()

    # Materials in storage room
    plywood2mm = Item(name='Plywood 2mm 900x600mm Sheet', location=storage, price=11.15)
    plywood2mm.save()

    mdf4mm = Item(name='MDF 4mm 900x600mm Sheet', location=storage, price=5.67)
    mdf4mm.save()

    acrylic5mm = Item(name='Acrylic 5mm 900x600mm Sheet', location=storage, price=19.34)
    acrylic5mm.save()

    # Supplies in assembly room
    woodGlue = Item(name='Wood Glue', location=assembly, price=9.0)
    woodGlue.save()

    nails1mm2cm = Item(name='Nails 1mm 2cm Long', location=assembly, price=0.7)
    nails1mm2cm.save()

    screws3mm3cm = Item(name='Wood Screws 3mm 3cm Long', location=assembly, price=0.8)
    screws3mm3cm.save()

    drill5mm = Item(name='Drill 5mm for Wood', location=assembly, price=5.05)
    drill5mm.save()

    # Electroncs items
    resistor200ohm = Item(name='Resistor SMT 200', location=electronics, price=0.2)
    resistor200ohm.save()

    resistor22k = Item(name='Resistor SMT 22K', location=electronics, price=0.2)
    resistor22k.save()

    openpir = Item(name='Sparkfun OPENPIR Motion Sensor', location=electronics, price=20.0)
    openpir.save()

    print('Database should now be filled with demo data.')
