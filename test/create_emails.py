import win32com.client as win32
import os

# Helper function to create .msg files
def create_msg(subject, body, category, index):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.Body = body
    directory = os.path.join(os.getcwd(), category)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'{category}_{index}.msg')
    mail.SaveAs(file_path)

# DELETE_MAIL examples
delete_mail_examples = [
    ("Gewinnen Sie jetzt ein iPhone!", "Herzlichen Glückwunsch! Sie haben die Chance, ein brandneues iPhone zu gewinnen. Klicken Sie hier, um teilzunehmen."),
    ("Dringend: Verlängern Sie Ihre Garantie", "Verlängern Sie Ihre Gerätegarantie jetzt und sparen Sie 50%."),
    ("Sonderangebot: 70% Rabatt auf alle Artikel", "Nur für kurze Zeit: Sparen Sie 70% auf alle Artikel in unserem Online-Shop."),
    ("Ihre Kreditkarte wurde belastet", "Ihre Kreditkarte wurde mit $500 belastet. Wenn Sie diese Transaktion nicht autorisiert haben, klicken Sie hier."),
    ("Gewinnen Sie einen Traumurlaub", "Nehmen Sie an unserer Umfrage teil und gewinnen Sie einen Traumurlaub für zwei Personen.")
]

# ANSWER_MAIL examples
answer_mail_examples = [
    ("Anfrage zu Projekt X", "Hallo, ich habe eine Frage zum Projekt X. Könnten Sie mir bitte die neuesten Updates und Informationen zukommen lassen?"),
    ("Feedback zu Ihrem letzten Bericht", "Könnten Sie bitte Ihr Feedback zu meinem letzten Bericht geben?"),
    ("Dringende Unterstützung benötigt", "Ich brauche dringend Ihre Unterstützung bei einem wichtigen Problem."),
    ("Fragen zur Rechnungsstellung", "Ich habe einige Fragen zu meiner letzten Rechnung. Können Sie mir bitte weiterhelfen?"),
    ("Koordination für den nächsten Workshop", "Können wir einen Termin für die Koordination unseres nächsten Workshops festlegen?")
]

# CREATE_MEETING examples
create_meeting_examples = [
    ("Einladung zum Meeting am 15. Juni", "Bitte nehmen Sie an unserem Meeting am 15. Juni um 10:00 Uhr teil. Thema: Projektfortschritt."),
    ("Besprechung zur Quartalsplanung", "Wir laden Sie herzlich zur Besprechung zur Quartalsplanung am 20. Juni um 14:00 Uhr ein."),
    ("Kick-off Meeting für neues Projekt", "Kick-off Meeting für das neue Projekt am 25. Juni um 9:00 Uhr. Bitte bestätigen Sie Ihre Teilnahme."),
    ("Teammeeting am Freitag", "Unser wöchentliches Teammeeting findet am Freitag um 11:00 Uhr statt. Bitte seien Sie pünktlich."),
    ("Kundentreffen am 30. Juni", "Treffen Sie uns am 30. Juni um 13:00 Uhr für eine Besprechung mit unserem wichtigsten Kunden.")
]

# USER_ACTION_NEEDED examples
user_action_needed_examples = [
    ("Genehmigung für Budgetanpassung erforderlich", "Bitte überprüfen und genehmigen Sie die vorgeschlagene Budgetanpassung für das nächste Quartal."),
    ("Unterschrift für Vertrag erforderlich", "Bitte unterschreiben Sie den beigefügten Vertrag und senden Sie ihn bis Ende der Woche zurück."),
    ("Aktualisierung Ihrer Kontoinformationen", "Bitte aktualisieren Sie Ihre Kontoinformationen bis zum 1. Juli."),
    ("Bestätigung der Teilnahme an der Konferenz", "Bitte bestätigen Sie Ihre Teilnahme an der Konferenz bis zum 15. Juni."),
    ("Überprüfung des Projektplans", "Bitte überprüfen und kommentieren Sie den beigefügten Projektplan.")
]

# READ_MAIL examples
read_mail_examples = [
    ("Newsletter Mai 2024", "Sehr geehrter Kunde, hier finden Sie unseren neuesten Newsletter mit wichtigen Informationen und Updates."),
    ("Wöchentlicher Team-Update", "Hier ist das wöchentliche Update unseres Teams mit allen wichtigen Neuigkeiten und Fortschritten."),
    ("Branchennews und Updates", "Bleiben Sie auf dem Laufenden mit den neuesten Nachrichten und Updates aus der Branche."),
    ("Interne Mitteilung: Neue Richtlinien", "Bitte lesen Sie die beigefügte interne Mitteilung zu den neuen Unternehmensrichtlinien."),
    ("Monatsbericht April 2024", "Der Monatsbericht für April 2024 ist jetzt verfügbar. Bitte lesen Sie die Details im Anhang.")
]

# Create DELETE_MAIL .msg files
for index, (subject, body) in enumerate(delete_mail_examples):
    create_msg(subject, body, "DELETE_MAIL", index + 1)

# Create ANSWER_MAIL .msg files
for index, (subject, body) in enumerate(answer_mail_examples):
    create_msg(subject, body, "ANSWER_MAIL", index + 1)

# Create CREATE_MEETING .msg files
for index, (subject, body) in enumerate(create_meeting_examples):
    create_msg(subject, body, "CREATE_MEETING", index + 1)

# Create USER_ACTION_NEEDED .msg files
for index, (subject, body) in enumerate(user_action_needed_examples):
    create_msg(subject, body, "USER_ACTION_NEEDED", index + 1)

# Create READ_MAIL .msg files
for index, (subject, body) in enumerate(read_mail_examples):
    create_msg(subject, body, "READ_MAIL", index + 1)
