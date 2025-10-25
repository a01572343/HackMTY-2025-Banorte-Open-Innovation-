import os
import shutil

# Path to the CSV file (same directory as this script)
csv_name = 'finanzas_personales.xlsx - in.csv'
script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, csv_name)

if not os.path.exists(csv_path):
    print(f"File not found: {csv_path}")
    raise SystemExit(1)

# create a backup
bak_path = csv_path + '.bak'
shutil.copyfile(csv_path, bak_path)
print(f'Backup created at: {bak_path}')

# read, replace, write
with open(csv_path, 'r', encoding='utf-8') as f:
    data = f.read()

new = data.replace('EducaciÃ³n', 'Educacion')
new = new.replace('NÃ³mina', 'Nomina')
new = new.replace('lÃ­nea', 'linea')

if new == data:
    print('No replacements necessary (no matching strings found).')
else:
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(new)
    print('Replacements applied successfully.')
