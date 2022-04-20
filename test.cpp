#include<iostream.h>
#include<conio.h>
#include<stdio.h>
#include<string.h>

class shape
{
public:
double h,ba;

shape()
{
h=0;
ba=0;
}

void get_data()
{
cout<<"\nEnter h and ba to compute are :";
cin>>h>>ba;
}

virtual void display_area()
{
}
};

class triangle : public shape
{
public:

void display_area()
{
cout<<h;
cout<<"\nArea of triangle = "<<(h*ba)/2;
}
};

class rectangle : public shape
{
public:

//redefining function display_area()
void display_area()
{
cout<<"\nArea of rectangle = "<<h*ba;
}
};
void main()
{
shape *s;
triangle t;
t.get_data();
s=&t;
s->display_area();
rectangle r;
r.get_data();
s=&r;
s->display_area();
getch();
}
