#include <iostream>
using namespace std;



int new_option;

void currency_converter(){

    cout << "Available options for currency conversion are:" << endl;

    cout << "1. Convert to USD" << endl;

    cout << "2. Convert to Euro" << endl;

    cout << "3. Convert to Japanese Yen" << endl;

    cout << "\n";

    

   

    int option;

    cout << "Your option: ";

    cin >> option;

    float inr;



    switch(option)

    {

       

        case 1:

            cout << "\nEnter the INR amount to convert into USD: ";

            cin >> inr;

            inr *= 0.012;



            cout << "The converted USD amount: " << inr << endl;

            cout << "Do you want to convert to a new currency?\nPress 1 to 'proceed' and 2 to 'exit' from here\n" << endl;

            cout << "Your option: ";

            cin >> new_option;

            if (new_option == 1){

                currency_converter();

            }

        break;

       

        

        case 2:

            cout << "\nEnter the INR amount to convert into EUR: ";

            cin >> inr;

            inr *= 0.011;



            cout << "The converted EUR amount: " << inr << endl;

            cout << "Do you want to convert to a new currency?\nPress 1 to 'proceed' and 2 to 'exit' from here\n" << endl;

            cout << "Your option: ";

            cin >> new_option;

            if (new_option == 1){

                currency_converter();

            }

        break;

       

        

        case 3:

            cout << "\nEnter the INR amount to convert into JPY: ";

            cin >> inr;

            inr *= 1.61;



            cout << "The converted JPY amount: " << inr << endl;

            cout << "Do you want to convert to a new currency??\nPress 1 to 'proceed' and 2 to 'exit' from here\n" << endl;

            cout << "Your option: ";

            cin >> new_option;

            if (new_option == 1){

                currency_converter();

            }

        break;

    }

}



int main()

{

    currency_converter();

    cout << "Thank you!";

    return 0;

}
