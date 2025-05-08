import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Крестики-нолики',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSwatch(primarySwatch: Colors.deepPurple),
      ),
      home: const TicTacToePage(),
    );
  }
}

class TicTacToePage extends StatefulWidget {
  const TicTacToePage({super.key});

  @override
  State<TicTacToePage> createState() => _TicTacToePageState();
}

class _TicTacToePageState extends State<TicTacToePage> {
  List<String> board = List.filled(9, '');
  String currentPlayer = 'X';

  void _handleTap(int index) {
    if (board[index].isNotEmpty) return;
    setState(() {
      board[index] = currentPlayer;
      if (_checkWin(currentPlayer)) {
        _showWinDialog(currentPlayer);
      } else if (!board.contains('')) {
        _showDrawDialog();
      }
      currentPlayer = currentPlayer == 'X' ? 'O' : 'X';
    });
  }

  bool _checkWin(String player) {
    const winPatterns = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];
    for (var pattern in winPatterns) {
      if (pattern.every((index) => board[index] == player)) {
        return true;
      }
    }
    return false;
  }

  void _showWinDialog(String player) {
    showDialog(
      context: context,
      builder:
          (context) => AlertDialog(
            title: Text('$player победил!'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  setState(() {
                    board = List.filled(9, '');
                  });
                },
                child: const Text('Играть снова'),
              ),
            ],
          ),
    );
  }

  void _showDrawDialog() {
    showDialog(
      context: context,
      builder:
          (context) => AlertDialog(
            title: const Text('Ничья!'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  setState(() {
                    board = List.filled(9, '');
                  });
                },
                child: const Text('Играть снова'),
              ),
            ],
          ),
    );
  }

  void _resetBoard() {
    setState(() {
      board = List.filled(9, '');
      currentPlayer = 'X';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Крестики-нолики'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _resetBoard),
        ],
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(16.0),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          mainAxisSpacing: 8.0,
          crossAxisSpacing: 8.0,
        ),
        itemCount: 9,
        itemBuilder: (context, index) {
          final player = board[index];
          final icon =
              player == 'X'
                  ? Icon(Icons.close, size: 64, color: Colors.blueAccent)
                  : player == 'O'
                  ? Icon(
                    Icons.circle_outlined,
                    size: 64,
                    color: Colors.redAccent,
                  )
                  : null;

          return GestureDetector(
            onTap: () => _handleTap(index),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.deepPurple.shade100,
                borderRadius: BorderRadius.circular(16.0),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    spreadRadius: 2,
                    blurRadius: 6,
                  ),
                ],
              ),
              child: Center(child: icon),
            ),
          );
        },
      ),
    );
  }
}
