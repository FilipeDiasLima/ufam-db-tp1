# ARQUIVO DE ENTRADA
import psycopg2
import re

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
	host="localhost",
	database="postgres",
	user="postgres",
	password="postgres",
	port='5432'
)

# Criação das tabelas
cur = conn.cursor()

# cur.execute("""
# 							CREATE TABLE grupos ( 
# 							id_grupo serial NOT NULL, 
# 							grupo TEXT, 
# 							PRIMARY KEY (id_grupo));
#             """)

# cur.execute("""
# 							CREATE TABLE produtos (
# 							asin TEXT NOT NULL, 
# 							titulo TEXT, 
# 							vendas int, 
# 							id_grupo int, 
# 							PRIMARY KEY (asin), 
# 							FOREIGN KEY (id_grupo) REFERENCES grupos (id_grupo));
#             """)

# cur.execute("""
# 							CREATE TABLE similares (
# 							id_sim serial NOT NULL, 
# 							asin TEXT, 
# 							asin_sim TEXT, 
# 							PRIMARY KEY (id_sim), 
# 							FOREIGN KEY (asin) REFERENCES produtos (asin));
#             """)

# cur.execute("""
# 							CREATE TABLE categorias (
# 							id_cat serial NOT NULL, 
# 							categoria TEXT, 
# 							PRIMARY KEY (id_cat));
#             """)

# cur.execute("""
# 							CREATE TABLE produtos_categorias (
# 							id_prodcat serial NOT NULL, 
# 							asin TEXT, 
# 							id_cat int, 
# 							PRIMARY KEY (id_cat), 
# 							FOREIGN KEY (asin) REFERENCES produtos (asin));
#             """)

# cur.execute("""
# 							CREATE TABLE clientes (
# 							id_cli serial NOT NULL, 
# 							cliente TEXT, 
# 							PRIMARY KEY (id_cli));
#             """)

# cur.execute("""
# 							CREATE TABLE avaliacoes(
# 							id_ava serial NOT NULL, 
# 							data date, 
# 							media int, 
# 							votos int, 
# 							util int, 
# 							id_cli int, 
# 							asin TEXT, 
# 							PRIMARY KEY (id_ava), 
# 							FOREIGN KEY (id_cli) REFERENCES clientes (id_cli), 
# 							FOREIGN KEY (asin) REFERENCES produtos (asin));
#             """)

# cur.execute("CREATE TABLE Product (id INTEGER PRIMARY KEY, asin VARCHAR(10) UNIQUE, title VARCHAR(500), group_name VARCHAR(50), sales_rank INTEGER);")

# cur.execute("CREATE TABLE Category (id SERIAL PRIMARY KEY, name VARCHAR(500), parent_id INTEGER, FOREIGN KEY (parent_id) REFERENCES Category(id));")

# cur.execute("CREATE TABLE ProductCategory (product_id INTEGER REFERENCES Product(id), category_id INTEGER REFERENCES Category(id), PRIMARY KEY (product_id, category_id));")

# cur.execute("CREATE TABLE ProductSimilarity (product_id INTEGER REFERENCES Product(id), similar_asin VARCHAR(10) REFERENCES Product(asin), PRIMARY KEY (product_id, similar_asin));")

# cur.execute("CREATE TABLE Review (id SERIAL PRIMARY KEY, product_id INTEGER REFERENCES Product(id), date DATE, customer_id VARCHAR(50), rating INTEGER, votes INTEGER, helpful INTEGER);")

# Abrir o arquivo .txt para leitura
with open('example.txt', 'r') as file:
    lines = file.readlines()

# Variáveis para armazenar as informações do item atual
current_id = None
current_asin = None
current_title = None
current_group = None
current_salesrank = None
current_similar = None
current_categories = None
current_reviews = None
total_reviews = None
total_downloaded = None
avg_rating = None
date_review = None
customer_review = None
rating_review = None
votes_review = None
helpful_review = None

# Loop pelas linhas do arquivo
for line in lines:
    # Remover espaços em branco no início e no final da linha
    line = line.strip()

    # Se a linha começar com "Id:", então é um novo item
    if line.startswith("Id:"):
        # Se já houver informações de um item anterior, adicione-as à tabela
        if current_id is not None:
            # Adicionar as informações do item atual à tabela, substitua "nome_da_tabela" pelo nome da tabela relevante
            # Exemplo de sintaxe de inserção em uma tabela SQL usando a biblioteca sqlite3
            # cur.execute("""
            #             INSERT INTO nome_da_tabela 
            #               	(id, asin, title, group, salesrank, similar, categories, reviews) 
            #                 VALUES (%(current_id)s, %(current_asin)s, %(current_title)s, %(current_group)s, %(current_salesrank)s, %(current_similar)s, %(current_categories)s, %(current_reviews)s)",
            #                	(current_id, current_asin, current_title, current_group, current_salesrank, current_similar, current_categories, current_reviews)
            #             """)
            print("Adicionado à tabela: ", current_id, "\n")
        
        # Extrair o novo ID do item
        current_id = int(line.split(":")[1].strip())
    elif line.startswith("ASIN:"):
        current_asin = line.split(":")[1].strip()
    elif line.startswith("title:"):
        current_title = line.split(":")[1].strip()
    elif line.startswith("group:"):
        current_group = line.split(":")[1].strip()
    elif line.startswith("salesrank:"):
        current_salesrank = int(line.split(":")[1].strip())
    elif line.startswith("similar:"):
        current_similar = line.split(":")[1].strip().split("  ")
    elif line.startswith("categories:"):
        current_categories = line.split(":")[1].strip().split("|")
    elif line.startswith("reviews: total:"):
        match = re.search(r'reviews: total: (\d+).*downloaded: (\d+).*avg rating: ([\d.]+)', line)
        if match:
            # Extrair os grupos de números correspondentes
            total_reviews = match.group(1)
            total_downloaded = match.group(2)
            avg_rating = match.group(3)
    elif line.startswith("20"):
        match = re.search(r'(\d+-\d+-\d+)\s+cutomer:\s+(\S+)\s+rating:\s+(\d+)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)', line)
        if match:
            date_review = match.group(1)
            customer_review = match.group(2)
            rating_review = int(match.group(3))
            votes_review = int(match.group(4))
            helpful_review = int(match.group(5))
            # Adicionar aqui a inserção de cada linha na tabela
            print(date_review, customer_review, rating_review, votes_review, helpful_review)
    else:
        continue
		
    print(current_id, current_asin, current_title, current_group, current_salesrank, current_similar, current_categories, date_review, total_reviews, total_downloaded, avg_rating)
# Adicionar as informações do último item à tabela
if current_id is not None:
    # Adicionar as informações do item atual à tabela, substitua "nome_da_tabela" pelo nome da tabela relevante
    # Exemplo de sintaxe de inserção em uma tabela SQL usando a biblioteca sqlite3
    # cur.execute("""
		# 						INSERT INTO nome_da_tabela 
		# 								(id, asin, title, group, salesrank, similar, categories, reviews) 
		# 								VALUES (%(current_id)s, %(current_asin)s, %(current_title)s, %(current_group)s, %(current_salesrank)s, %(current_similar)s, %(current_categories)s, %(current_reviews)s)",
		# 								(current_id, current_asin, current_title, current_group, current_salesrank, current_similar, current_categories, current_reviews)
		# 						""")
    print("Adicionado à tabela: ", current_id, "\n")


conn.commit()
conn.close()