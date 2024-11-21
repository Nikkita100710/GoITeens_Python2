input_1 = int(input("Введіть кількість грошей: "))
finish = 0
while input_1 != 0:
   if input_1 - 500 >= 0:
       input_1 -= 500
       # print(500)
       finish += 1

   elif input_1 - 200 >= 0:
       input_1 -= 200
       finish += 1
       # print(200)


   elif input_1 - 100 >= 0:
       input_1 -= 100
       finish += 1
       # print(100)


   elif input_1 - 50 >= 0:
       input_1 -= 50
       finish += 1
       # print(20)


   elif input_1 - 20 >= 0:
       input_1 -= 20
       finish += 1
       # print(20)


   elif input_1 - 10 >= 0:
       input_1 -= 10
       # print(10)
       finish += 1
   else:
       finish = -1
       break


print(finish)

