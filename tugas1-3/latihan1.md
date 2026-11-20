# Tugas 1 — Membaca Syntax Tree, Eksplorasi Tree-sitter Playground
# Langkah 1
### Percobaan 1: x = 1
module [0, 0] - [1, 0]
  expression_statement [0, 0] - [0, 5]
    binary_operator [0, 0] - [0, 5]
      left: identifier [0, 0] - [0, 1]
      right: integer [0, 4] - [0, 5]

### Percobaan 2: x = 1 + 2
module [0, 0] - [1, 0]
  expression_statement [0, 0] - [0, 9]
    assignment [0, 0] - [0, 9]
      left: identifier [0, 0] - [0, 1]
      right: binary_operator [0, 4] - [0, 9]
        left: integer [0, 4] - [0, 5]
        right: integer [0, 8] - [0, 9]

Saat dibandingkan dengan percobaan 1, node yang bertambah pada percobaan 2 yaitu node binary_operator pada bagian right dari parent assignment. Node tersebut memiliki dua child yaitu pada bagian left dan right dengan tipe integer yang merepresentasikan 1 + 2.

### Percobaan 3: print(x)
module [0, 0] - [1, 0]
  expression_statement [0, 0] - [0, 8]
    call [0, 0] - [0, 8]
      function: identifier [0, 0] - [0, 5]
      arguments: argument_list [0, 5] - [0, 8]
        identifier [0, 6] - [0, 7]

Saat dibandingkan dengan percobaan 1, node yang bertambah pada percobaan 3 yaitu node arguments dengan tipe argument_list yang memiliki satu child yaitu identifier yang merepresentasikan x.

# Langkah 2
### fungsi 
module 
  function_definition
    name: identifier
    parameters: parameters       
      identifier
    body: block
      return_statement
        binary_operator
          left: identifier
          right: identifier

### if/else
module 
  expression_statement 
    assignment 
      left: identifier 
      right: integer
  if_statement
    condition: comparison_operator 
      identifier 
      integer 
    consequence: block
      expression_statement 
        call 
          function: identifier 
          arguments: argument_list 
            string

### class
module 
  class_definition
    name: identifier 
    body: block 
      function_definition 
        name: identifier
        parameters: parameters 
          identifier 
          identifier 
        body: block 
          return_statement 
            binary_operator 
              left: identifier 
              right: identifier 

