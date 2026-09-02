from flask import Flask, jsonify, request

app = Flask(__name__)

#Уточнение (1) для меня здесь на первое время, по дизайну первому там просто 3 отдельных иконки и каждая по 30 яиц
#Для теста POST оставил 2 продукта из 3
#Вынес в отдельный лист чтобы пополнять лист продуктов, мало ли
products = [
        {"id": 1, "name": "30 egg (1)"},
        {"id": 2, "name": "30 egg (2)"}
    ]

@app.route("/") 
def home():
    return jsonify({"message": "Hello from team Ballest Balls!"})

@app.route("/products", methods=["GET"]) #Получить данные без изменений
def get_products():
    return jsonify(products)

#В целом не нужно именно для продуктов, ибо у нас один вид, но вписал это просто для того чтобы понять и изучить
@app.route("/products", methods=["POST"]) #создать новые данные
def add_products():
    data = request.get_json()
    new_products = {
        "id": len(products) + 1,
        "name": data.get("name")
    }
    if isinstance(data.get("name"), str) and data.get("name").strip(): #проверка на строку и то что это не пустая строка или же пробелы
        products.append(new_products) #Добавляем новый продукт добавленный с помощью кода выше в лист, который лежит в начале кода
        return jsonify({"message": "Product added", "product": new_products}), 201 
    else: 
        return jsonify({"message": "Hujna peredelivaj"}), 400
    

if __name__ == "__main__":
    app.run(debug=True)    