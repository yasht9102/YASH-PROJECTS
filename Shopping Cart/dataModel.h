#include<bits/stdc++.h>

// product ,items ,cart


class Product{
    int id;
    std::string name;
    int price;

public:

    Product(int id, std::string name,int price){
        this->id=id;
        this->name=name;
        this->price=price;
    }

    std::string getDisplayName(){
        return std::to_string(id)+")" + name + ": Rs " + std::to_string(price);
    }
    int getId(){
        return id;
    }

    friend class Item;

};


class Item{
    Product product;
    int quantity;

public: 

    Item(Product p,int q):product(p),quantity(q){};

    int getTotalPrice(){
        return quantity*product.price;
    }

    std::string getItemInfo(){
        return std::to_string(quantity) + " x " + product.name + "---> Rs." + std::to_string(quantity*product.price);
    }

};

class Cart{






};




























