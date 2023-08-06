# BanelePackage

This is my first straightforward package for performing mathematics computations like summing digits etc, and also concatinating strings

## Instalation

To instal this package just run the following command:

```shell
pip install BanelePackage
```

```py


from BanelePackage import numbers, strings

# output
print("The sum of the two numbers is: ", numbers.add(4, 2))
print("The product of the two numbers is: ", numbers.mult(4, 2))
print("The difference of the two numbers is: ", numbers.sub(2, 4))
print("The quotient of the two numbers is: ", numbers.div(2, 4))


print("The two strings combined yields: ",
      strings.concatenate("BaneleOf", "@stro"))
print("The string in reverse: ", strings.reverseString("Banele"))

```
