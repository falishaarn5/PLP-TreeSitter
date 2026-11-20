module.exports = grammar({
  name: 'filter',

  extras: $ => [/\s/],

  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison,
      $.and_expression,
      $.or_expression,
      $.parenthesized,
      $.not_expression,
      $.in_expression
    ),

    and_expression: $ => prec.left(2, seq(
      field('left', $._expr),
      'and',
      field('right', $._expr)
    )),

    or_expression: $ => prec.left(1, seq(
      field('left', $._expr),
      'or',
      field('right', $._expr)
    )),

    parenthesized: $ => seq(
      '(',
      field('expression', $._expr),
      ')'
    ),

    not_expression: $ => prec(3, seq(
      'not',
      field('expression', $._expr)
    )),

    in_expression: $ => seq(
      field('left', $.identifier),
      'in',
      '(',
      field('value', $._value),
      repeat(seq(',', field('value', $._value))),
      ')'
    ),
    
    comparison: $ => seq(
      field('left', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('right', $._value)
    ),

    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
    number: $ => /[0-9]+/,
    boolean: $ => choice('true', 'false'),
    _value: $ => choice(
      $.string,
      $.number,
      $.boolean
    ),
  }
});