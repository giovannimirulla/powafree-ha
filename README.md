# Powafree H4 Cloud Integration for Home Assistant

Questa è un'integrazione personalizzata (Custom Component) per Home Assistant che permette di monitorare e controllare le batterie da balcone **Powafree H4** (BigBlue) interfacciandosi con le loro API Cloud ufficiali.

Poiché il dispositivo H4 non espone porte locali sulla rete LAN, questa integrazione simula l'app ufficiale per estrarre i dati via HTTP.

## 🌟 Funzionalità
- **Sensori in Lettura:**
  - Stato della Batteria (SOC %, SOH %)
  - Produzione Solare (W) totale, PV1 e PV2
  - Generazione Giornaliera e Totale (kWh)
  - Temperature
- **Controlli (Sperimentali):**
  - Switch per abilitare/disabilitare l'immissione in rete
  - Slider per impostare la potenza massima in uscita (0-800W)

## 📥 Installazione tramite HACS
Il metodo consigliato per l'installazione è tramite [HACS](https://hacs.xyz/).

1. Apri HACS nel tuo pannello di Home Assistant.
2. Clicca sul menu a tre puntini (in alto a destra) e seleziona **Custom repositories**.
3. Incolla l'URL di questo repository: `https://github.com/giovannimirulla/powafree-ha`
4. Seleziona la categoria **Integration**.
5. Clicca su **Add**.
6. Ora cerca `Powafree` in HACS, clicca su **Download** e riavvia Home Assistant.

## ⚙️ Configurazione
1. Vai su **Impostazioni** > **Dispositivi e servizi**.
2. Clicca su **Aggiungi Integrazione** in basso a destra.
3. Cerca **Powafree H4 Cloud Integration**.
4. Inserisci la tua **Email** e **Password** che usi nell'app POWAFREE Solar Hub.
5. Fatto! I dispositivi e le entità appariranno automaticamente.

## ⚠️ Disclaimer
Questa integrazione non è ufficiale e non è affiliata in alcun modo a BigBlue o Powafree. Utilizza chiamate API reverse-ingegnerizzate che potrebbero cambiare in qualsiasi momento. Usa a tuo rischio e pericolo.
