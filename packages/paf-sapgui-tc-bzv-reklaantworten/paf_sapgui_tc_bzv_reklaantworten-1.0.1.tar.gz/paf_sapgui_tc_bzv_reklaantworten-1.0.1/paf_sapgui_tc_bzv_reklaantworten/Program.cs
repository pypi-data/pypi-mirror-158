using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using gAnmeldung = AS.Auto.Web.Sap.Gui.Komponenten.Allgemein.Anmeldung;
using gAllgemein = AS.Auto.Web.Sap.Gui.Allgemein;
using gHelfer = AS.Helfer;
using Prot = AS.Helfer.Protokollierung;
using gKonfig = AS.Helfer.Konfiguration;
using gCIC = AS.Auto.Web.Sap.Gui.Komponenten.Vx.Cic;
using System.Threading;
using System.Collections.ObjectModel;
using AS.Helfer;
using Newtonsoft.Json;

namespace TF.Web.Sap.Gui.NichtUFTD
{
    class BZV_Reklaantworten
    {
        private static readonly int cintAnzahlSchleifen = 0;
        private static int cintAnzahlVorfaelle = 0;
        
        static void Main()
        {

            //Konfiguration des Protokolls
            Prot.ProtokollstufenStrings(gKonfig.LeseGruppeOhneTagnamen("Protokollstufen", "Protokollstufe").ToArray<string>());
            Prot.Konfiguration("BZV_Reklaantworten", "Datei", "Konsole");

            ArrayList larrlAlleFehler = new ArrayList();

            Prot.Info("Starte Testfall 'BZV_Reklaantworten'");

            Vorbereitungen();
            Anmeldung();

            //Weitere_Bearbeitung();
            //gCIC.Details_zur_Position.Text_aendern("1010210748", "Neuer Text", false);

            //while (Transaktion_vorbereiten())
            //{
            //    cintAnzahlSchleifen++;
            //    Dictionary<int, ArrayList> ldictDaten = Analyse_Tabelle();

            //    foreach (KeyValuePair<int, ArrayList> lkvplWerte in ldictDaten)
            //    {
            //        larrlAlleFehler.Add(lkvplWerte.Value);
            //    }

            //    CIC(ldictDaten);
            //    Abweisen(ldictDaten);
            //    Weitere_Bearbeitung();
            //}

            if (Transaktion_vorbereiten())
            {
                Dictionary<int, ArrayList> ldictDaten = Analyse_Tabelle();

                if (ldictDaten.Count > 0) { 

                    foreach (KeyValuePair<int, ArrayList> lkvplWerte in ldictDaten) larrlAlleFehler.Add(lkvplWerte.Value);

                    CIC(ldictDaten);
                    Abweisen(ldictDaten);
                } else
                {
                    Prot.Info("Keine Einträge zur Verarbeitung gefunden.");
                }
            }     else
            {
                Prot.Info("Keine Einträge zur Verarbeitung gefunden.");
            }
            Protokoll(cintAnzahlSchleifen, cintAnzahlVorfaelle, larrlAlleFehler);

            gAllgemein.Elemente.Sitzung_beenden();



            // ZJKTA_NB_RKLSM

            //     Gruppenschöüssel AI BZV
            //     Status ABO-interface U

            // Anzhal der Zeilen zählen(bei mehr als 10 Warnmeldung)
            // Zahlen zu gesamtzahl


            // Doppelklick auf Zeile
            // BZHRNR Nummer kopieren, letzte 1 Weg
            // ANTWTTXT kopieren
            // ENZLRKLDAT2 kopieren

            // CIC mit Nummer -> In Detials -> in Text -> an erster Stelle mit heutigem Datum den kopierten Text und das kopierte Datum

            // in Transaktion In Spalte AI u anklicken abweisen



            //Nachdem alle abgearbeitet sind in Transaktion ZJKTA_AI_LD_RKLSM
            // Variante KAIRKBIN_U
            // Ausführen und ggf.Fehlerfenster bearbeiten
            // Schleife + 1


            // mehr als zwei Schleifen -> Fehlermeldung
            // mehr als 10 gesamtzeilen -> Fehlermeldung

        }
        /// <summary>
        ///  Verarbeitet das Protkoll, welches das Ergebnis der Ausführung per E-Mail sendet bzw. als Jira-Punkt erstellt
        /// </summary>
        /// <param name="Schleifen">Anzahl der Schleifen, die für die Verarbeitung gebraucht wurden</param>
        /// <param name="Vorfaelle">Wieviele Vorfälle sind während des Laufs aufgetaucht</param>
        /// <param name="AlleFehler">Übergabe aller aufgetauchten (und auch bearbeiteten) Fehler</param>
        /// <returns></returns>
        private static void Protokoll(int Schleifen, int Vorfaelle, ArrayList AlleFehler)
        {
            gHelfer.Konfiguration.Zugangsdatum ldictEmails = gKonfig.Zugangsdaten("emails_senden");

            Prot.Info("Sende das normale Protokoll!");
            gHelfer.Konfiguration.EmailInhalt lEmailInhalt = gKonfig.Emailinhalt("Email", "Protokoll");

            AS.Helfer.EMail.Sende(
                SendenBenutzername: ldictEmails.Benutzer,
                SendenPasswort: ldictEmails.Passwort,
                Absender: ldictEmails.Benutzer,
                Empfaenger: gKonfig.Emailempfaenger("Email", "Empfaenger", "Protokoll"),
                Betreff: gHelfer.EMail.Pruefdatum("BZV_Reklaantworten") + " " + lEmailInhalt.Betreff,
                Text: lEmailInhalt.Anrede + "<br /><br />" + lEmailInhalt.Text + TextFuerNachrichten("Email", AlleFehler, Schleifen, Vorfaelle) + "<br /><br />Lieben Gruß<br/>Deine Automatisierung ;-)<br />" + gKonfig.Signaturen("ses_allgemein"),
                Anhaenge: (new string[] { Prot.Pfad_zur_Datei() })
                );

            //Fehlermeldung
            if (Schleifen > 2 || Vorfaelle > 20)
            {
                lEmailInhalt = gKonfig.Emailinhalt("Email", "Fehlermeldung");
                Prot.Info("Es wurden mehr als 2 Schleifen bzw. mehr als 20 Vorfaelle gefunden, sende eine Fehlermeldung!");
                AS.Helfer.EMail.Sende(
                    SendenBenutzername: ldictEmails.Benutzer,
                    SendenPasswort: ldictEmails.Passwort,
                    Absender: ldictEmails.Benutzer,
                    Empfaenger: gKonfig.Emailempfaenger("Email", "Empfaenger", "Fehlermeldung"),
                    Betreff: gHelfer.EMail.Pruefdatum("BZV_Reklaantworten-Fehler") + " " + lEmailInhalt.Betreff,
                    Text: lEmailInhalt.Anrede + "<br /><br />" + lEmailInhalt.Text + "Es wurden " + cintAnzahlSchleifen.ToString() + " Schleifen mit insgesamt " + cintAnzahlVorfaelle.ToString() + " gefunden!<br />" + gKonfig.Signaturen("ses_allgemein"),
                    Anhaenge: (new string[] { Prot.Pfad_zur_Datei() })
                );

                AS.Helfer.Jira.Bearbeiter("sync_alm_tech");
                AS.Helfer.Jira.Typ("Testfall");
                AS.Helfer.Jira.Status(gHelfer.Jira.Jirastatus.Testfall.Fehlgeschlagen);
                AS.Helfer.Jira.Stichworte("Monitoring", "BZV_Reklaantworten");
                AS.Helfer.Jira.Zusammenfassung(AS.Helfer.EMail.Pruefdatum("BZV_Reklaantworten"));
                AS.Helfer.Jira.Text("h1. FEHLER \r\n" + TextFuerNachrichten("Jira", AlleFehler, Schleifen, Vorfaelle));
                AS.Helfer.Jira.Neu();
            }
            else
            {
                AS.Helfer.Jira.Bearbeiter("sync_alm_tech");
                AS.Helfer.Jira.Typ(gHelfer.Jira.Jiratyp.Testfall);
                AS.Helfer.Jira.Status(gHelfer.Jira.Jirastatus.Testfall.Erfolgreich);
                AS.Helfer.Jira.Stichworte("Monitoring", "BZV_Reklaantworten");
                AS.Helfer.Jira.Zusammenfassung(AS.Helfer.EMail.Pruefdatum("BZV_Reklaantworten"));
                AS.Helfer.Jira.Text(TextFuerNachrichten("Jira", AlleFehler, Schleifen, Vorfaelle));
                AS.Helfer.Jira.Neu();
            }
        }
        /// <summary>
        /// Der Text, welcher in der Funktion "Protokoll" benötigt wird, wird hier erstellt
        /// </summary>
        /// <param name="Was">Für was soll der Text erstellt werden (Email/Jira)</param>
        /// <param name="AlleFehler">Übergabe der Fehler, um sie im Text verarbeiten zu können</param>
        /// <param name="Schleifen">Übergabe der durchlaufenen Schleifen</param>
        /// <param name="Vorfaelle">Übergabe der Anzahl der Vorfälle</param>
        /// <returns>string</returns>
        private static string TextFuerNachrichten(string Was, ArrayList AlleFehler, int Schleifen, int Vorfaelle)
        {
            string lstrText = "Ich habe " + (Schleifen + 1).ToString() + " Schleifen gedreht und dabei " + Vorfaelle.ToString() + " Vorfälle gefunden!<br />";
            if (AlleFehler.Count > 0)
            {
                lstrText += ((Was == "Email") ? "<ul>" : "");
                foreach (ArrayList larrlFehler in AlleFehler)
                {
                    lstrText += ((Was == "Email") ? "<li>" : "") + "Objektnummer: " + larrlFehler[3] +
                        ", VBELN: " + larrlFehler[0].ToString().Substring(0, larrlFehler[0].ToString().Length - 1) +
                        ", Text: " + larrlFehler[1] +
                        ", Datum: " + larrlFehler[2].ToString().Substring(6, 2) + "." + larrlFehler[2].ToString().Substring(4, 2) + "." + larrlFehler[2].ToString().Substring(0, 4) + " (" + larrlFehler[2] + ")" + ((Was == "Email") ? "</li>" : "");
                }
                lstrText += ((Was == "Email") ? "</ul>" : "");
            }
            else
            {
                lstrText += ((Was == "Email") ? "<b>" : "*") + "Es wurden keine Fehler gefunden" + ((Was == "Email") ? "</b>" : "*");
            }
            return lstrText;
        }
        private static void Vorbereitungen()
        {
            Prot.Info("Vorbereitungen");
        }
        private static void Anmeldung()
        {
            gHelfer.Konfiguration.Zugangsdatum ldictZugangsdaten = gKonfig.Zugangsdaten("SAP_V30_ckoeste1");
            gAnmeldung.Benutzername = ldictZugangsdaten.Benutzer;
            gAnmeldung.Passwort = ldictZugangsdaten.Passwort;

            switch (gKonfig.Lese("Konfiguration", "System").ToLower())
            {
                case "v30": gAnmeldung.Systemname = gAnmeldung.Sap_Systeme.V30; break;
                case "v35": gAnmeldung.Systemname = gAnmeldung.Sap_Systeme.V35; break;
            }

            Prot.Info("Anmeldung am System '" + gAnmeldung.Systemname + "' mit dem Benutzer '" + gAnmeldung.Benutzername + "' und dem Passwort '" + gAnmeldung.Passwort.Substring(0, 2) + "..." + "'");

            gAnmeldung.Sichtbar = true;
            gAnmeldung.Anmelden(gAllgemein.Elemente.Sitzungstypen.Chrome);
        }
        //private static void Weitere_Bearbeitung()
        //{
        //    AS.Auto.Web.Sap.Gui.Allgemein.Transaktion.Setze("ZJKTA_AI_LD_RKLSM");
        //    gAllgemein.Variante.aktiviere("KAIRKBIN_U");
        //    Thread.Sleep(2000);
        //    gAllgemein.Schaltflaeche.Ausfuehren();
        //    gAllgemein.Fenster.existiert_weiter(1);
        //}
        private static void Abweisen(Dictionary<int, ArrayList> Werte)
        {
            Prot.Info("Weise die bearbeiteten Aufträge in der ZJKTA_NB_RKLSM ab");
            AS.Auto.Web.Sap.Gui.Allgemein.Transaktion.Setze("ZJKTA_NB_RKLSM");
            gAllgemein.Fenster.WarteAuf("Nachbearbeitung Loader - Reklamationen");

            AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Selektion.Gruppenschluessel_AI().SendKeys("BZV");
            AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Selektion.Status_Abo_Interface().SendKeys("U");
            

            foreach (ArrayList larrlWerte in Werte.Values)
            {
                Prot.Info(larrlWerte[3].ToString());
                AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Selektion.Objektnummer().Clear();
                AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Selektion.Objektnummer().SendKeys(larrlWerte[3].ToString());
                AS.Auto.Web.Sap.Gui.Allgemein.Taste.F8();
                gAllgemein.Elemente.WarteAufElement(gAllgemein.Tabellen.Namen.SE16);
                gAllgemein.Tabellen.NeuBenannteTabelle("se16");
                gAllgemein.Tabellen.Zelle(1, 3, "se16").Click();
                AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Tabelle.Fehler_im_Nachbearbeitungsdialog.Abweisen().Click();
                Thread.Sleep(2000);
                AS.Auto.Web.Sap.Gui.Allgemein.Schaltflaeche.Zurueck();
                gAllgemein.Fenster.WarteAuf("Nachbearbeitung Loader - Reklamationen");
            }
        }
        private static void CIC(Dictionary<int, ArrayList> Werte)
        {
            Prot.Info("Verarbeitung im CIC");

            foreach (KeyValuePair<int, ArrayList> lkvplWerte in Werte)
            {
                ArrayList larrlWerte = lkvplWerte.Value;
                string lstrText = DateTime.Now.ToString("dd.MM.yyyy - HH:mm") +
                    " : " + larrlWerte[2].ToString().Substring(6) +
                    "." + larrlWerte[2].ToString().Substring(4, 2) +
                    "." + larrlWerte[2].ToString().Substring(0, 4) + " [Automatik SyMa] " +
                    " -> " + larrlWerte[1];

                Prot.Info("Verarbeitung im CIC! VBELN = " + larrlWerte[0].ToString() + ", Text: " + lstrText);

                gCIC.Details_zur_Position.Text_aendern((larrlWerte[0].ToString().Length == 10) ? larrlWerte[0].ToString() : larrlWerte[0].ToString().Substring(0, 10), lstrText);
            }
        }
        private static Dictionary<int, ArrayList> Analyse_Tabelle()
        {
            Prot.Info("Analysiere Tabelle");
            Dictionary<int, ArrayList> ldictErgebnisse = new Dictionary<int, ArrayList>();

            gAllgemein.Tabellen.NeuBenannteTabelle("se16");

            int lintReihen = AS.Auto.Web.Sap.Gui.Allgemein.Tabellen.Reihenanzahl("se16");

            for (int lintReihenzaehler = 1; lintReihenzaehler <= lintReihen; lintReihenzaehler++)
            {
                gAllgemein.Elemente.WarteAufElement(gAllgemein.Tabellen.Namen.SE16);
                Prot.Info("Reihe " + lintReihenzaehler);
                AS.Auto.Web.Sap.Gui.Allgemein.Taste.Doppelklick(AS.Auto.Web.Sap.Gui.Allgemein.Elemente.Tabellenzelle(lintReihenzaehler, 1, "se16"));
                gAllgemein.Elemente.WarteAufElement(gAllgemein.Tabellen.Namen.SE16_Detail);
                gAllgemein.Tabellen.NeuBenannteTabelle("se16_detail", gAllgemein.Tabellen.Namen.SE16_Detail);

                ldictErgebnisse.Add(lintReihenzaehler, new ArrayList() {
                    AS.Auto.Web.Sap.Gui.Allgemein.Tabellen.Zellenwert(6, 2, "se16_detail"),
                    AS.Auto.Web.Sap.Gui.Allgemein.Tabellen.Zellenwert(19, 2, "se16_detail"),
                    AS.Auto.Web.Sap.Gui.Allgemein.Tabellen.Zellenwert(14, 2, "se16_detail"),
                    AS.Auto.Web.Sap.Gui.Allgemein.Tabellen.Zellenwert(1,2, "se16_detail")
                });
                cintAnzahlVorfaelle++;
                AS.Auto.Web.Sap.Gui.Allgemein.Taste.Zurueck();
            }

            //Objektnummer 1,2
            //VBELN = 6,2
            //Text = 19,2
            //Datum = 15,2

            return ldictErgebnisse;

        }
        private static bool Transaktion_vorbereiten()
        {
            Prot.Info("Schaue in Transaktion ZJKTA_NB_RKLSM nach Einträgen");
            AS.Auto.Web.Sap.Gui.Allgemein.Transaktion.Setze("ZJKTA_NB_RKLSM");
            gAllgemein.Fenster.WarteAuf("Nachbearbeitung Loader - Reklamationen");
            
            AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Selektion.Gruppenschluessel_AI().SendKeys("BZV");
            AS.Auto.Web.Sap.Gui.Elemente.Vx.Transaktionen.ZJKTA_NB_RKLSM.Selektion.Status_Abo_Interface().SendKeys("U");
            AS.Auto.Web.Sap.Gui.Allgemein.Taste.F8();
            gAllgemein.Fenster.WarteAuf("Tabellenbrowser");
            if (gAllgemein.Fenster.ExistiertWeiter(1)) return false;
            return true;
        }
    }
}
