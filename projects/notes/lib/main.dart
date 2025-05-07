import 'package:flutter/material.dart';
import 'package:sqlite3/sqlite3.dart';
import 'package:sqlite3/sqlite3.dart' as sqlite3;
// import 'package:path/path.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Заметки',
      theme: ThemeData(primarySwatch: Colors.deepPurple),
      home: const NotesPage(),
    );
  }
}

class Note {
  final int id;
  final String title;
  final String content;

  Note({required this.id, required this.title, required this.content});

  factory Note.fromRow(sqlite3.Row row) {
    return Note(
      id: row['id'] as int,
      title: row['title'] as String,
      content: row['content'] as String,
    );
  }
}

class NotesDatabase {
  late Database _db;

  Future<void> initDB() async {
    final Directory dir = await getApplicationDocumentsDirectory();
    final String path = p.join(dir.path, 'notes.db');

    _db = sqlite3.sqlite3.open(path);
    _createTables();
  }

  void _createTables() {
    _db.execute('''
      CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
      )
    ''');
  }

Future<List<Note>> getNotes() async {
  final List<Note> notes = [];
  final rows = _db.select('SELECT * FROM notes ORDER BY id DESC');
  for (var row in rows) {
    notes.add(Note.fromRow(row));
  }
  return notes;
}

Future<int> insertNote(String title, String content) async {
  final stmt = _db.prepare('INSERT INTO notes(title, content) VALUES (?, ?)');
  stmt.execute([title, content]);
  stmt.dispose();
  return _db.lastInsertRowId;
}

  Future<void> deleteNote(int id) async {
    final stmt = _db.prepare('DELETE FROM notes WHERE id = ?');
    stmt.execute([id]);
    stmt.dispose();
  }
}

class NotesPage extends StatefulWidget {
  const NotesPage({super.key});

  @override
  State<NotesPage> createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  late Future<List<Note>> futureNotes;
  final NotesDatabase db = NotesDatabase();

  @override
  void initState() {
    super.initState();
    db.initDB();
    futureNotes = db.getNotes();
  }

  void _addNote() async {
    await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const AddNotePage()),
    );
    setState(() {
      futureNotes = db.getNotes();
    });
  }

  void _deleteNote(int id) async {
    await db.deleteNote(id);
    setState(() {
      futureNotes = db.getNotes();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Мои заметки')),
      body: FutureBuilder<List<Note>>(
        future: futureNotes,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Text('Ошибка: ${snapshot.error}');
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Нет заметок'));
          } else {
            final notes = snapshot.data!;
            return ListView.builder(
              itemCount: notes.length,
              itemBuilder: (context, index) {
                final note = notes[index];
                return ListTile(
                  title: Text(note.title),
                  subtitle: Text(note.content),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete),
                    onPressed: () => _deleteNote(note.id),
                  ),
                );
              },
            );
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addNote,
        tooltip: 'Добавить заметку',
        child: const Icon(Icons.add),
      ),
    );
  }
}

class AddNotePage extends StatefulWidget {
  const AddNotePage({super.key});

  @override
  State<AddNotePage> createState() => _AddNotePageState();
}

class _AddNotePageState extends State<AddNotePage> {
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _contentController = TextEditingController();

  final NotesDatabase db = NotesDatabase();

  @override
  void dispose() {
    _titleController.dispose();
    _contentController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    db.initDB(); // Переподключаемся к БД
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Добавить заметку')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: 'Заголовок'),
            ),
            TextField(
              controller: _contentController,
              decoration: const InputDecoration(labelText: 'Содержание'),
              maxLines: 5,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          if (_titleController.text.isNotEmpty ||
              _contentController.text.isNotEmpty) {
            await db.insertNote(
              _titleController.text,
              _contentController.text,
            );
            Navigator.pop(context);
          }
        },
        child: const Icon(Icons.save),
      ),
    );
  }
}