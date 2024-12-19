#include "dataModel.h"


std::vector<Product> allProducts={
    Product (1,"apple",26),
    Product (2,"mango",16),
    Product (3,"gauva",36),
    Product (4,"banana",56),
    Product (5,"strawberry",29),
    Product (6,"pinaaple",44),
    Product (7,"kiwi",51),
};


Product* chooseProduct(){

    // display the list of products
    std::string prodList;
    std::cout<<"Available products: "<<'\n';    

    for(auto product : allProducts){
        
        prodList.append(product.getDisplayName());
        std::cout<<product.getDisplayName()<<'\n';
    }

    // std::cout<<prodList <<'\n';

    std::cout<<"###########################"<<'\n';

    std::cout<<"please enter your choice: ";
    int choice;
    std::cin>>choice;

    for(int i=0;i<allProducts.size();i++){
        if(allProducts[i].getId() == choice){
            return &allProducts[i];
            // break;
        }
    }

    std::cout<<"Product not found"<<'\n';
    return NULL;
}



int main(){

    // Product p(1,"apple",26);
    // std::cout<<p.getDisplayName()<<'\n';

    // Item fruit(p,2);
    // std::cout<<fruit.getItemInfo()<<'\n';

     char action;
     while(true){

        std::cout<<"Select a action: "<<'\n';
        std::cout<<"(a) Add item "<<'\n';
        std::cout<<"(b) View cart "<<'\n';
        std::cout<<"(c) Checkout "<<'\n';

         std::cin>>action;

         if(action == 'a'){

            Product *product=chooseProduct();
            if(product != NULL){
                std::cout<<"Added to cart"<<product->getDisplayName()<<'\n';
            }


         }
         else if(action == 'v'){


         }

         else if(action == 'c'){

         }   


     }   


    return 0;
}
























