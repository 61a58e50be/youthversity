# Youthversity



Eine Lernplattform, auf der Jugendliche allein oder in Gruppen OER zu Themen anlegen können, die sie interessieren, auf OER anderer User zugreifen und somit ihr Wissen austauschen können.


![#wirvsvirus logo](docs/wirvsvirus_logo.png)




## Datamodel



- Content types

  - Text
  - Slides
  - Bilder
  - Videos

- Kategorien / Themenbereiche

- User Accounts

  - Types Schüler/Lehrer





## Design

Website

​	- Python3, Django



Textinhalte einfach als Markdown/WYSIWYG eingeben und in DB speichern.

Bilder auf einem Fileserver



### Funktionalitäten

- Login
- Registrierung  + Accounts
  - Lehrer- und SchülerAccounts
- Post erstellen, berarbeiten + löschen
- Posts kommentieren
  - reddit Style?
- Voting System für Posts
  - nur Upvotes
  - hinzufügen und entfernen eines eigenen Likes
- Melden von Posts
- Themen-Kategorien für Posts
  - erstmal nur Schulfächer
- personalisierte Feed?
  - Fächer abonnieren?
- Posts sich selber speichern
- Anzeige
  - Filter nach Kategorien, Sprachen?
  - Suche nach Titel
  - sortieren nach Erstellungsdatum
  - etc
- Frontend mit adaptive resizing
- Lokalisierung? i18n

## First Steps

1. Datenmodell entwerfen
2. Django Grundstuktur
3.



## Sonstiges

- Moderation
  - melden-Funktion
- Kommentare zu jedem Post/Lerneinheit
- Lehrer?
  - Können auch eine Hürde darstellen für Schüler.
  - Sollten vllt nicht an ihre Klasse gebunden sein, sondern wild durch die Plattform durch moderieren?
- Wikipedia-Prinzip für mehr Rechte, für die, die besondern hervorstehen?
- Warum lädt überhaupt jemand was hoch?
  - Lehrer schicken es an ihre Klassen?
  - Klassen eventuell repräsentiert im System?
    - Sichtbarkeit von Beitragen default lieber nicht auf Klassen beschränkt.
- Emojis freischalten durch (gute?) Posts - Gamification und Ansporn für die Schüler, auch Inhalte zu produzieren.
- verifizierte Antworten in Threads hervorheben? -> wie bei Stackoverflow
- Forum für Diskussionen/Fragen zu klären beim Erstellen von Posts
- Beiträge auch nach Themen/Kategorien sortieren/anzeigen
- Einladungslinks für Lehrer, den sie an ihre Schüler geben können.
-





## Zukünftige Ideen

- Kollaboration
- Lehrer verifizieren
