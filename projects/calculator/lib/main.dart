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
        brightness: Brightness.dark,
        primaryColor: Colors.black,
        scaffoldBackgroundColor: Colors.black,
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
          final expression = _input.replaceAll('×', '*').replaceAll('÷', '/');
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
    const buttonStyle = TextStyle(fontSize: 28, color: Colors.white);
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
                style: const TextStyle(fontSize: 48, color: Colors.white),
              ),
            ),
          ),
          for (var row in [
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
                              onPressed: () => _onButtonPressed(value),
                              style: ElevatedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(
                                  vertical: 24,
                                ),
                                backgroundColor: Colors.grey[850],
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(24),
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
