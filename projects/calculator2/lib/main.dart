import 'package:flutter/material.dart';
import 'package:math_expressions/math_expressions.dart';
import 'dart:math';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Калькулятор',
      theme: ThemeData(
        brightness: Brightness.light,
        primaryColor: Colors.white,
        scaffoldBackgroundColor: Colors.white,
        textTheme: const TextTheme(
          bodyMedium: TextStyle(fontSize: 28, color: Colors.black),
          displayLarge: TextStyle(fontSize: 48, color: Colors.black),
        ),
      ),
      home: const CalculatorPage(),
    );
  }
}

class CalculatorPage extends StatefulWidget {
  const CalculatorPage({super.key});

  @override
  State<CalculatorPage> createState() => _CalculatorPageState();
}

class _CalculatorPageState extends State<CalculatorPage> {
  String _input = '';
  String _output = '0';
  List<String> _history = [];

  int factorial(int n) {
    if (n < 0) throw ArgumentError('Negative factorial is not defined');
    int result = 1;
    for (var i = 1; i <= n; i++) {
      result *= i;
    }
    return result;
  }

  String replaceFactorials(String expr) {
    return expr.replaceAllMapped(RegExp(r'(\d+)!'), (match) {
      final n = int.parse(match.group(1)!);
      final fact = factorial(n);
      return fact.toString();
    });
  }

  String formatResult(num result) {
    if (result is double && result == result.roundToDouble()) {
      return result.toInt().toString();
    }
    return result.toString();
  }

  void _onButtonPressed(String value) {
    setState(() {
      if (value == 'C') {
        _input = '';
        _output = '0';
      } else if (value == '=') {
        try {
          String expression = _input
              .replaceAll('×', '*')
              .replaceAll('÷', '/')
              .replaceAll('π', '3.14159265359')
              .replaceAll('e', '2.71828182846')
              .replaceAllMapped(RegExp(r'(sin|cos|tan)\((.*?)\)'), (match) {
                final func = match.group(1);
                final arg = match.group(2);
                return '${func}(${double.parse(arg!) * pi / 180})';
              })
              .replaceAllMapped(RegExp(r'√(\d+(\.\d+)?)'), (match) {
                final number = match.group(1);
                return 'sqrt($number)';
              })
              .replaceAllMapped(RegExp(r'\((.*?)\)\^(\d+\.?\d*)'), (match) {
                final base = match.group(1);
                final exponent = match.group(2);
                return 'pow($base, $exponent)';
              });

          expression = replaceFactorials(expression);

          // ignore: deprecated_member_use
          final parser = Parser();
          final result = parser
              .parse(expression)
              .evaluate(EvaluationType.REAL, ContextModel());

          final formattedResult = formatResult(result);
          final calculation = '$_input = $formattedResult';
          _history.insert(0, calculation);
          _output = formattedResult;
        } catch (e) {
          _output = 'Error';
        }
      } else {
        _input += value;
        _output = _input;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final buttonStyle = Theme.of(context).textTheme.bodyMedium;

    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          Expanded(
            flex: 4,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              alignment: Alignment.topRight,
              child: ListView.builder(
                itemCount: _history.length,
                itemBuilder: (context, index) {
                  return Text(
                    _history[index],
                    style: const TextStyle(fontSize: 24, color: Colors.grey),
                  );
                },
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Container(
              alignment: Alignment.bottomRight,
              padding: const EdgeInsets.all(24.0),
              child: Text(
                _output,
                style: Theme.of(context).textTheme.displayLarge,
              ),
            ),
          ),
          for (var row in [
            ['√', '^', 'e', '!'],
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+'],
          ])
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children:
                  row
                      .map(
                        (value) => Expanded(
                          child: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: ElevatedButton(
                              onPressed: () {
                                if (value == '!') {
                                  setState(() {
                                    _input += '!';
                                    _output = _input;
                                  });
                                } else {
                                  _onButtonPressed(value);
                                }
                              },
                              style: ElevatedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(
                                  vertical: 24,
                                ),
                                backgroundColor:
                                    value.length == 1 &&
                                            value.codeUnitAt(0) >= 48 &&
                                            value.codeUnitAt(0) <= 57
                                        ? const Color.fromARGB(
                                          255,
                                          221,
                                          221,
                                          221,
                                        )
                                        : Colors.orange,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                ),
                              ),
                              child: Text(value, style: buttonStyle),
                            ),
                          ),
                        ),
                      )
                      .toList(),
            ),
        ],
      ),
    );
  }
}
