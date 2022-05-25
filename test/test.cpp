#include <iostream>
#include <fstream>
#include <string>
using namespace std;

class Person
{
private:
 string name;
 int age;
public:
 void setdata(string name, int age){
  this->name = name;
  this->age = age;
 }
 void getdata(){
  cout << "Name: " << name << endl;
  cout << "Age: " << age << endl;
 }
 int get_age() {
  return age;
 }
 string get_name() {
  return name;
 }

};


int main()
{

 Person p;
 string name;
 int age, n;

 ofstream outfile;
 outfile.open("Person.dat", ios::binary | ios::app);
 cout << "Input name and age: "; cin >> name >> age; 
 p.setdata(name, age); 
 outfile.write((char*)&p, sizeof(p));
 outfile.close();
 ifstream infile;
 infile.open("Person.dat", ios::binary);
 infile.seekg(0, ios::beg);
 while (infile.read((char*)&p, sizeof(p)))
 {
  p.getdata();
 }
 infile.close();

    int a;
 cout << "Enter the command: " << endl;
 cout << "1. Determine the age of the specified person " << endl;
 cout << "2. Determine the name if age is known" << endl;
 cout << "3. Delete a record" << endl;
 cout << "4. Add a record to a specific position" << endl;

 cin >> a;
 switch (a) {
     case 1:
         cout << "Enter the age: "; cin >> age;
         ifstream infile;
            infile.open("Person.dat", ios::binary);
            infile.seekg(0, ios::beg);
        while (infile.read((char*)&p, sizeof(p)))
        {
            if (p.get_age() == age) {
                cout << p.get_name() << endl;
            }

        }
        infile.close();

        break;
 }

 system("pause");
 return 0;
}