# derivative-calculator
Symbolic differentiation tool that includes its own parser

![Tests](https://github.com/scfenton6/derivative-calculator/actions/workflows/tests.yml/badge.svg)

## Description

This repository contains a symbolic differentiation tool written in python that includes:

- It's own LL(1) parser to convert a string representing a mathematical function into an Abstract Syntax Tree.

- A tool that performs symbolic differentiation on the AST applying the chain rule recursively to produce an AST containing the function's derivative.

- An interpreter that takes an AST representing a mathematical function and returns the function in string format.

Both the symbolic differentiation tool and the interpreter simplifiy binary arithmetic operations between numbers, multiplication and division by one, and addition, substraction and multiplication by zero. Additionally, the interpreter simplifies expressions containing an arbitrary number of prefix signs.

## Motivation

The purpose to start this project was for me to learn about parsing. To this end, I followed the series [Let's Build A Simple Interpreter](https://ruslanspivak.com/lsbasi-part1). The series explains in detail how to build a parser and interpreter from scratch, accompanied with code snippets, and the code for my parser is mainly based on it. 

To give the parser a use, I decided to write code for a tool that would use the tree structure of the Abstract Syntax Tree produced by the parser to perform symbolic differentiation by doing a DFS traversal on it. The notation and general structure I used to write the symbolic differentiation tool is based on Subsection 2.3.2 or the book [Structure and Interpretation of Computer Programs, 2nd ed.](https://web.mit.edu/6.001/6.037/sicp.pdf).

## How to use

To use the derivative calculator, run the interface.py file and enter a string containing a mathematical function, as well as a single character string containing the variable that you want to derivate respect to.
