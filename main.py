import requests
from bs4 import BeautifulSoup
import csv

# URL de base pour les recherches Best Buy
base_url = 'https://www.bestbuy.com/site/searchpage.jsp?st=cell+phone&intl=nosplash'

# En-têtes pour imiter un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def fetch_page(url):
    """Effectue une requête GET sur l'URL spécifiée et retourne le contenu de la page."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return None

def parse_products(html):
    """Analyse le HTML et extrait les informations sur les produits."""
    soup = BeautifulSoup(html, 'html.parser')
    product_elements = soup.find_all('li', {'class': 'sku-item'})  # Mise à jour du sélecteur
    products = []

    if not product_elements:
        print("Aucun produit trouvé sur la page.")
    else:
        for product in product_elements:
            title = product.select_one('h4.sku-title a')
            price = product.select_one('div.priceView-customer-price span')
            rating = product.select_one('div.c-ratings-reviews span.c-reviews')  # Mise à jour du sélecteur pour les notes
            # reviews = product.select_one('span.c-reviews')  # Mise à jour du sélecteur pour les avis

            title_text = title.get_text(strip=True) if title else "Titre non disponible"
            price_text = price.get_text(strip=True) if price else "Prix non disponible"
            rating_text = rating.get_text(strip=True) if rating else "Évaluation non disponible"
            # reviews_text = reviews.get_text(strip=True) if reviews else "Avis non disponibles"
            
            products.append({
                'Title': title_text,
                'Price': price_text,
                'Rating': rating_text,
                # 'Reviews': reviews_text
            })

    return products

def main():
    """Exécute le processus de récupération et de transformation des données."""
    products = []
    max_products = 150
    page = 1

    # Scraping des produits depuis Best Buy
    while len(products) < max_products:
        url = f"{base_url}&page={page}"
        html = fetch_page(url)
        if html is None:
            break

        page_products = parse_products(html)
        if not page_products:
            break

        products.extend(page_products)
        page += 1

    products = products[:max_products]

    # Transformation et enregistrement des données dans un fichier CSV
    output_file = 'transformed_products.csv'

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Brand', 'Description', 'Price', 'Rating']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            # Séparer la première partie du titre (la marque) du reste
            title_parts = product['Title'].split(' ', 1)
            brand = title_parts[0]
            description = title_parts[1] if len(title_parts) > 1 else ''
            
            # Nettoyer le prix et l'évaluation
            price = product['Price'].replace('$', '').replace(',', '')
            rating = product['Rating'].strip('()')
            
            # Écrire la nouvelle ligne dans le fichier CSV
            writer.writerow({
                'Brand': brand,
                'Description': description,
                'Price': price,
                'Rating': rating
            })

    print(f"Le fichier transformé a été enregistré sous le nom '{output_file}'.")

if __name__ == "__main__":
    main()
