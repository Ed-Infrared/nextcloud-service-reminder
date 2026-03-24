# Nextcloud Service Reminder

Een Python-toepassing die automatisch morgen geplande afspraken van Nextcloud bemerkt, relevante service-informatie uit PDF-serviceboeken haalt, converteert naar WhatsApp-compatibele afbeeldingen en stuurt deze naar vooraf gedefinieerde ontvangers.

## Technische specifics

- **Technologieën**: Python, CalDAV, PyMuPDF, Pillow, requests, python-dotenv
- **Planning**: Gedistilleerd in fasen (in witnessesolus) met tests
- **Vereisten**: Virtuele omgeving, specifieke afhankelijkheden
- **Functionaliteit**: Automatische serviceherinneringen via WhatsApp

## Repository-inhoud

- `src/` - Hoofdcode voor de toepassing
- `diensten/` - PDF-serviceboeken met technische informatie
- `Documents/` - Planning en documentatie
- `tests/` - Testcases en uitvoeringscript

## Installatie

```bash
# Creëer virtuele omgeving
python3 -m venv venv
source venv/bin/activate

# Installeer afhankelijkheden
pip install -r requirements.txt

# Voer test uit om verificatie uit te voeren
./tests/run_tests.sh
```