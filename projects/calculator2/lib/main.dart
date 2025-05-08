import 'package:flutter/material.dart';
import 'package:math_expressions/math_expressions.dart';

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

  void _onButtonPressed(String value) {
    setState(() {
      if (value == 'C') {
        _input = '';
        _output = '0';
      } else if (value == '=') {
        try {
          final expression = _input
              .replaceAll('×', '*')
              .replaceAll('÷', '/')
              .replaceAll('√', 'sqrt')
              .replaceAll('^', 'pow')
              .replaceAll('π', '3.14159265359')
              .replaceAll('e', '2.71828182846');
          // ignore: deprecated_member_use
          final parser = Parser();
          final result = parser
              .parse(expression)
              .evaluate(EvaluationType.REAL, ContextModel());
          _output = result.toString();
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
    final accentColor = Colors.orange;
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
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
            ['sin', 'cos', 'tan', 'π'],
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
                                  try {
                                    final num = int.parse(_input);
                                    _output =
                                        List.generate(
                                          num,
                                          (i) => i + 1,
                                        ).fold(1, (a, b) => a * b).toString();
                                    _input = _output;
                                  } catch (e) {
                                    _output = 'Error';
                                  }
                                } else {
                                  _onButtonPressed(value);
                                }
                              },
                              style: ElevatedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(
                                  vertical: 24,
                                ),
                                backgroundColor:
                                    value == '=' ||
                                            value == '+' ||
                                            value == '-' ||
                                            value == '×' ||
                                            value == '÷' ||
                                            value == '^' ||
                                            value == '√' ||
                                            value == '!' ||
                                            value == 'sin' ||
                                            value == 'cos' ||
                                            value == 'tan' ||
                                            value == 'π' ||
                                            value == 'e'
                                        ? accentColor
                                        : Colors.grey[300],
                                foregroundColor:
                                    value == '=' ||
                                            value == '+' ||
                                            value == '-' ||
                                            value == '×' ||
                                            value == '÷' ||
                                            value == '^' ||
                                            value == '√' ||
                                            value == '!' ||
                                            value == 'sin' ||
                                            value == 'cos' ||
                                            value == 'tan' ||
                                            value == 'π' ||
                                            value == 'e'
                                        ? Colors.white
                                        : Colors.black,
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
