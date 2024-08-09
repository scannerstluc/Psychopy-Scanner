import pkg_resources

# Spécifiez le chemin vers votre fichier requirements.txt
requirements_path = 'requirements.txt'

# Lire les dépendances à partir du fichier requirements.txt
with open(requirements_path, 'r') as file:
    requirements = file.readlines()

# Nettoyer et extraire le nom du paquet
requirements = [line.strip().split('>=')[0] for line in requirements if line.strip() and not line.startswith('#')]

# Vérifier les versions des paquets installés
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
missing_packages = []
version_info = []

for requirement in requirements:
    if requirement in installed_packages:
        version_info.append(f"{requirement}: version installée est {installed_packages[requirement]}")
    else:
        missing_packages.append(requirement)

# Afficher les résultats
if version_info:
    print("Informations de version pour les paquets installés :")
    for info in version_info:
        print(info)
if missing_packages:
    print("Paquets manquants :")
    for pkg in missing_packages:
        print(pkg)
