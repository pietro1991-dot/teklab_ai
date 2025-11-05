# 📋 TEKLAB CHUNKS - PIANO STRATEGICO DI CREAZIONE

**Obiettivo**: Creare una knowledge base completa per il chatbot Teklab AI che copra tutti i prodotti, tecnologie e casi d'uso.

---

## 🎯 STRATEGIA GENERALE

### Principi di creazione chunks:
1. **1 chunk = 1 concetto chiaro** (non mescolare argomenti)
2. **Ogni prodotto ha 2-4 chunks**:
   - Overview generale del prodotto
   - Specifiche tecniche dettagliate
   - Installazione e setup
   - Troubleshooting e FAQ specifiche
3. **Q&A separate** per ogni prodotto (5-10 domande)
4. **Chunks applicativi** per settori/usi specifici

---

## 📦 PRODOTTI - ANALISI DOCUMENTI

### **TK SERIES - Oil Level Controllers**

#### **TK1+ (Entry Level - Alarm Only)**
- **Documenti disponibili**:
  - `TK1+ Oil Level Switch - Teklab.eu.mhtml`
  - `TK1_PDF-SHORT.pdf`
  
- **Chunks necessari (4)**:
  1. ✅ `tk1_plus_oil_level_switch.json` - Overview generale (CREATO)
  2. ⭐ `tk1_plus_technical_specs.json` - Specifiche dettagliate (pin-out, dimensioni, materiali)
  3. ⭐ `tk1_plus_installation_guide.json` - Installazione passo-passo, cablaggio
  4. ⭐ `tk1_plus_applications.json` - Casi d'uso tipici, esempi di installazione

- **Q&A necessarie (8)**:
  1. Quando usare TK1+ invece di TK3+?
  2. Può essere usato con refrigeranti diversi?
  3. Come cablare l'allarme?
  4. Compatibilità con oli sintetici?
  5. Temperatura massima operativa?
  6. Differenza tra versioni 46/80/130 bar?
  7. Può sostituire un vecchio galleggiante meccanico?
  8. Garanzia e durata prevista?

---

#### **TK3+ (Automatic Refill - 3 versioni)**
- **Documenti disponibili**:
  - `TK3+ 46 bar Version - Teklab.eu.mhtml` + `TK3-@46bar_PDF-SHORT.pdf`
  - `TK3+ 80 bar Version - Teklab.eu.mhtml` + `TK3-@80bar_PDF-SHORT.pdf`
  - `TK3+ 130 bar Version - Teklab.eu.mhtml` + `TK3@130bar_PDF-SHORT.pdf`

- **Chunks necessari (12 - 4 per versione)**:

  **TK3+ 46bar (R134a, R22)**:
  1. ✅ `tk3_plus_46bar_oil_level_controller.json` - Overview (CREATO)
  2. ⭐ `tk3_plus_46bar_wiring_installation.json` - Cablaggio dettagliato, schemi elettrici
  3. ⭐ `tk3_plus_46bar_refrigerants.json` - Compatibilità refrigeranti, applicazioni HVAC
  4. ⭐ `tk3_plus_46bar_troubleshooting.json` - Diagnostica errori, LED meanings, soluzioni

  **TK3+ 80bar (R410A, R407C)**:
  1. ✅ `tk3_plus_80bar.json` - Overview (CREATO)
  2. ⭐ `tk3_plus_80bar_pressure_safety.json` - Safety margins, burst pressure, materiali
  3. ⭐ `tk3_plus_80bar_compressor_compatibility.json` - Marche compressori, modelli rack
  4. ⭐ `tk3_plus_80bar_maintenance.json` - Manutenzione preventiva, pulizia sensore

  **TK3+ 130bar (CO2 Transcritical)**:
  1. ✅ `tk3_plus_130bar.json` - Overview CO2 systems (CREATO)
  2. ⭐ `tk3_plus_130bar_co2_specifics.json` - Caratteristiche uniche CO2, alta pressione
  3. ⭐ `tk3_plus_130bar_supermarket_racks.json` - Applicazioni GDO, multi-compressor
  4. ⭐ `tk3_plus_130bar_regulations.json` - Normative CO2, F-Gas, certificazioni

- **Q&A necessarie (15)**:
  1. Come scegliere tra 46/80/130 bar?
  2. TK3+ funziona con miscele zeotropiche?
  3. Quanto tempo impiega il refill automatico?
  4. Può gestire più compressori in parallelo?
  5. Differenza tra TK3+ e TK4?
  6. Compatibile con oli POE/PVE?
  7. Come interpretare i LED di status?
  8. Distanza massima cavi solenoide?
  9. Resistenza a vibrazioni compressore?
  10. Calibrazione necessaria dopo installazione?
  11. Compatibile con CO2 subcritico?
  12. Pressione differenziale minima richiesta?
  13. Protezione IP rating?
  14. Può funzionare con alimentazione 24V DC?
  15. Backup manuale se sensore fallisce?

---

#### **TK4 / TK4 MODBUS (Advanced - Temperature + Communication)**
- **Documenti disponibili**:
  - TK4: `TK4 46/80/130 bar Version` (3 MHTML + 3 PDF)
  - TK4 MODBUS: `TK4 MODBUS 46/80/130bar Version` (3 MHTML + 3 PDF)

- **Chunks necessari (16 - 8 standard + 8 MODBUS)**:

  **TK4 Standard (no MODBUS)**:
  1. ⭐ `tk4_46bar_overview.json` - Caratteristiche base TK4 vs TK3+
  2. ⭐ `tk4_80bar_temperature_monitoring.json` - Funzione misura temperatura, allarmi
  3. ⭐ `tk4_130bar_display_interface.json` - Display LCD, navigazione menu
  4. ⭐ `tk4_all_advanced_alarms.json` - Allarmi multipli, soglie personalizzabili

  **TK4 MODBUS (Communication)**:
  1. ✅ `tk4_modbus_advanced_features.json` - Overview MODBUS (CREATO)
  2. ⭐ `tk4_modbus_rs485_wiring.json` - Cablaggio RS485, terminazioni, schermature
  3. ⭐ `tk4_modbus_register_map.json` - Registro MODBUS completo, R/W addresses
  4. ⭐ `tk4_modbus_scada_integration.json` - Integrazione con PLC/SCADA, esempi
  5. ⭐ `tk4_modbus_remote_configuration.json` - Configurazione remota, parametri
  6. ⭐ `tk4_modbus_multi_device.json` - Network con più TK4, indirizzamento
  7. ⭐ `tk4_modbus_data_logging.json` - Logging storico temperatura/livello
  8. ⭐ `tk4_modbus_troubleshooting.json` - Diagnostica comunicazione, errori comuni

- **Q&A necessarie (20)**:
  1. Vale la pena TK4 MODBUS vs TK4 standard?
  2. Baud rate supportati RS485?
  3. Quanti TK4 su un bus MODBUS?
  4. Compatibile protocolli oltre MODBUS RTU?
  5. Software necessario per configurazione?
  6. Può inviare email allarmi?
  7. Integrazione con Building Management System?
  8. Accuratezza misura temperatura?
  9. Storico dati salvato internamente?
  10. Alimentazione PoE possibile?
  11. Upgrade firmware da remoto?
  12. Compatibilità con Schneider/Siemens PLC?
  13. Cybersecurity features?
  14. Cloud connectivity?
  15. Differenza display TK4 vs TK4 MODBUS?
  16. Temperature probe tipo e range?
  17. Ritardo allarme temperatura configurabile?
  18. Multi-language display?
  19. Password protection settings?
  20. Datasheet MODBUS disponibile?

---

### **LC SERIES - Level Switches**

#### **LC-PS (Basic Relay)**
- **Documenti disponibili**:
  - `LC-PS Level Switch - Teklab.eu.mhtml`
  - `LC-PS_PDF-SHORT.pdf`

- **Chunks necessari (3)**:
  1. ✅ `lc_ps_level_switch.json` - Overview (CREATO)
  2. ⭐ `lc_ps_applications_water_glycol.json` - Applicazioni acqua/glicole, chiller
  3. ⭐ `lc_ps_relay_wiring.json` - Schemi cablaggio relay, NC/NO logic

- **Q&A necessarie (6)**:
  1. Differenza LC-PS vs LC-PH?
  2. Può controllare pompa direttamente?
  3. Compatibile con liquidi corrosivi?
  4. Distanza max cavi relay?
  5. Protezione sovracorrente relay?
  6. Versione IP68 disponibile?

---

#### **LC-PH (Dual Relay)**
- **Documenti disponibili**:
  - `LC-PH Level Switch up to 120bar - Teklab.eu.mhtml`
  - `LC-PH_PDF-SHORT.pdf`

- **Chunks necessari (3)**:
  1. ⭐ `lc_ph_dual_relay.json` - Overview doppio relay
  2. ⭐ `lc_ph_pump_control.json` - Controllo pompe primarie/backup
  3. ⭐ `lc_ph_high_low_alarms.json` - Allarmi livello alto/basso simultanei

- **Q&A necessarie (6)**:
  1. Applicazioni tipiche dual relay?
  2. Ritardi temporizzazione relay?
  3. Logica failsafe integrata?
  4. Compatibile con inverter pompe?
  5. Test funzionale relay?
  6. Durata vita relay (cicli)?

---

#### **LC-XP (Relay + 4-20mA)**
- **Documenti disponibili**:
  - `LC-XP Level Switch up to 120bar - Teklab.eu.mhtml`
  - `LC-XP-oil-level-switch.pdf`
  - `LC-XT_LC-XP_PDF-SHORT.pdf` (combined)

- **Chunks necessari (4)**:
  1. ✅ `lc_xp_analog_output.json` - Overview (CREATO)
  2. ⭐ `lc_xp_4_20ma_calibration.json` - Calibrazione loop corrente, scaling
  3. ⭐ `lc_xp_plc_integration.json` - Connessione PLC, esempi Ladder
  4. ⭐ `lc_xp_analog_diagnostics.json` - Troubleshooting 4-20mA, open/short circuit

- **Q&A necessarie (8)**:
  1. Come calibrare uscita 4-20mA?
  2. Precisione misura analogica?
  3. Compatibile con ingressi 0-10V?
  4. Distanza massima cavo 4-20mA?
  5. Alimentazione loop powered?
  6. Protezione sovratensione analogica?
  7. Output 0-20mA vs 4-20mA?
  8. Resistenza loop max?

---

#### **LC-XT (Relay + 4-20mA + Temperature)**
- **Documenti disponibili**:
  - `LC-XT Level Switch - Teklab.eu.mhtml`
  - `LC-XT_LC-XP_PDF-SHORT.pdf` (combined)

- **Chunks necessari (4)**:
  1. ✅ `lc_xt_temperature_monitoring.json` - Overview (CREATO)
  2. ⭐ `lc_xt_dual_parameter.json` - Monitoraggio livello+temperatura simultaneo
  3. ⭐ `lc_xt_thermal_protection.json` - Allarmi temperatura, protezione compressore
  4. ⭐ `lc_xt_scada_integration.json` - Invio dati multipli a SCADA

- **Q&A necessarie (6)**:
  1. Sensore temperatura tipo (PT100/NTC)?
  2. Accuratezza ±°C temperatura?
  3. Dual 4-20mA outputs o singolo?
  4. Ritardo allarme temperatura?
  5. Registrazione min/max temperatura?
  6. Compatibile con datalogger?

---

### **ALTRI PRODOTTI**

#### **K25 4-20mA Level Switch**
- **Documenti disponibili**:
  - `K25 4-20 mA Level Switch - Teklab.eu.mhtml`
  - `K25_PDF-SHORT.pdf`

- **Chunks necessari (3)**:
  1. ⭐ `k25_compact_analog.json` - Overview versione compatta
  2. ⭐ `k25_vs_lc_comparison.json` - K25 vs LC-XP differenze
  3. ⭐ `k25_oem_applications.json` - Applicazioni OEM, private label

- **Q&A necessarie (4)**:
  1. Quando scegliere K25 vs LC-XP?
  2. Dimensioni ridotte K25?
  3. Disponibile customizzazione K25?
  4. Prezzo K25 vs LC?

---

#### **Rotalock (RLK) Level Switch**
- **Documenti disponibili**:
  - `Rotalock (RLK) Level Switch - Teklab.eu.mhtml`
  - `ROTALOCK-RLK02_PDF-SHORT.pdf`

- **Chunks necessari (3)**:
  1. ⭐ `rlk_rotalock_connector.json` - Overview connettore Rotalock
  2. ⭐ `rlk_quick_installation.json` - Installazione rapida senza saldature
  3. ⭐ `rlk_retrofit_upgrade.json` - Retrofit impianti esistenti

- **Q&A necessarie (5)**:
  1. Cos'è un connettore Rotalock?
  2. Compatibilità diametri Rotalock?
  3. Tenuta garantita senza brasatura?
  4. Differenza RLK vs sensore filettato?
  5. Applicazioni marine/navali?

---

#### **Adapters**
- **Documenti disponibili**:
  - `Adapters - Teklab.eu.mhtml`
  - `Adapters_PDF-SHORT.pdf`

- **Chunks necessari (2)**:
  1. ⭐ `adapters_catalog.json` - Catalogo adattatori disponibili
  2. ⭐ `adapters_custom_solutions.json` - Soluzioni custom, filettature speciali

- **Q&A necessarie (4)**:
  1. Adattatori per filettature NPT?
  2. Adattatori per alta pressione disponibili?
  3. Materiali adattatori (ottone/acciaio)?
  4. Tempi produzione adattatori custom?

---

## 🔬 TECNOLOGIA - CHUNKS TRASVERSALI

### **IR Technology - Come Funziona**
- **Documenti disponibili**:
  - `Technical notes/how it works.txt`
  - `Electro Optical Liquid Sensors - Electro Optical Level Switches _ Teklab.mhtml`

- **Chunks necessari (5)**:
  1. ✅ `ir_technology_how_it_works.json` - Principio rifrazione luce (CREATO)
  2. ⭐ `ir_optical_components.json` - LED, fotodiodo, prisma ottico
  3. ⭐ `ir_signal_processing.json` - Elaborazione segnale, immunità disturbi
  4. ⭐ `ir_accuracy_factors.json` - Fattori che influenzano accuratezza ±2mm
  5. ⭐ `ir_vs_capacitive.json` - Confronto IR vs sensori capacitivi

- **Q&A necessarie (8)**:
  1. Perché IR è meglio di galleggiante meccanico?
  2. IR funziona con liquidi torbidi?
  3. IR influenzato da schiuma?
  4. Usura componenti ottici nel tempo?
  5. Pulizia prisma ottico necessaria?
  6. IR compatibile con oli molto viscosi?
  7. Frequenza controllo livello IR?
  8. Consumo energetico IR vs altri sensori?

---

### **Mechanical vs IR - Business Case**
- **Chunks necessari (3)**:
  1. ✅ `ir_vs_mechanical_floats.json` - TCO analysis (CREATO)
  2. ⭐ `float_failure_modes.json` - Modalità rottura galleggianti
  3. ⭐ `roi_calculation_tool.json` - Tool calcolo ROI switch to IR

- **Q&A necessarie (6)**:
  1. ROI tipico passaggio da float a IR?
  2. Costi manutenzione galleggiante vs IR?
  3. Downtime evitato con IR?
  4. Case study clienti?
  5. Garanzia Teklab vs concorrenti?
  6. Costo iniziale IR vs float?

---

## 🏭 APPLICAZIONI - SETTORI SPECIFICI

### **Refrigerazione Industriale**
- **Chunks necessari (4)**:
  1. ✅ `compressor_oil_management_application.json` - Rack compressori (CREATO)
  2. ⭐ `cold_storage_warehouses.json` - Celle frigorifere, temperature estreme
  3. ⭐ `food_processing_plants.json` - Industria alimentare, igiene HACCP
  4. ⭐ `ice_rinks_applications.json` - Piste ghiaccio, glicole

---

### **HVAC - Climatizzazione**
- **Chunks necessari (3)**:
  1. ⭐ `chiller_applications.json` - Gruppi frigoriferi, acqua refrigerata
  2. ⭐ `vrf_vrv_systems.json` - Sistemi VRF multi-split
  3. ⭐ `rooftop_units.json` - RTU commerciali

---

### **ATEX - Ambienti Esplosivi**
- **Documenti disponibili**:
  - `Atex Infrared Level Sensors - Atex Infrared Switch Sensors _ Teklab.mhtml`
  - `EEx Level Switch. ATEX Metallic IR sensor up to 100°C - Teklab.eu.mhtml`
  - `EX-Electro-optic_PDF-SHORT.pdf`

- **Chunks necessari (6)**:
  1. ✅ `atex_metallic_ir_sensor.json` - Sensore metallico ATEX (CREATO)
  2. ✅ `atex_explosive_atmosphere_applications.json` - Ammoniaca refrigerazione (CREATO)
  3. ⭐ `atex_certification_explained.json` - Ex d IIC T6 spiegazione
  4. ⭐ `atex_zone_classification.json` - Zone 1/2, criteri selezione
  5. ⭐ `atex_installation_requirements.json` - Requisiti installazione, cablaggio
  6. ⭐ `atex_maintenance_safety.json` - Manutenzione sicura ATEX

- **Q&A necessarie (10)**:
  1. Cos'è certificazione Ex d IIC T6?
  2. Differenza Zone 1 vs Zone 2?
  3. ATEX obbligatorio per ammoniaca?
  4. Ispezioni periodiche ATEX?
  5. Può essere installato da tecnico non certificato?
  6. Documentazione necessaria per ATEX?
  7. Costo ATEX vs standard?
  8. ATEX compatibile con R290 (propano)?
  9. Temperature classe T4 vs T6?
  10. Gruppi gas IIA vs IIC?

---

### **Marine & Offshore**
- **Chunks necessari (3)**:
  1. ⭐ `marine_refrigeration.json` - Celle frigo navi, pescherecci
  2. ⭐ `offshore_platforms.json` - Piattaforme petrolifere, vibrazioni
  3. ⭐ `naval_certifications.json` - Certificazioni navali (Lloyd's, RINA)

---

## 🛠️ SUPPORTO - GUIDE TECNICHE

### **Installation Guides**
- **Chunks necessari (4)**:
  1. ⭐ `general_installation_guide.json` - Procedura installazione generica
  2. ⭐ `wiring_diagrams_comprehensive.json` - Schemi cablaggio tutti modelli
  3. ⭐ `mounting_positions_guide.json` - Posizioni montaggio ottimali
  4. ⭐ `commissioning_checklist.json` - Checklist messa in servizio

---

### **Troubleshooting**
- **Chunks necessari (5)**:
  1. ✅ `common_troubleshooting_guide.json` - Problemi comuni (CREATO)
  2. ⭐ `led_error_codes.json` - Codici errore LED, significato
  3. ⭐ `sensor_cleaning_procedure.json` - Pulizia prisma ottico
  4. ⭐ `relay_chattering_solutions.json` - Soluzioni relay che vibra
  5. ⭐ `false_alarms_diagnostics.json` - Falsi allarmi, cause e soluzioni

---

### **Selection & Comparison**
- **Chunks necessari (4)**:
  1. ✅ `product_selection_guide_pressure_rating.json` - Guida selezione pressione (CREATO)
  2. ✅ `tk3_vs_tk4_comparison_guide.json` - Confronto TK3+ vs TK4 (CREATO)
  3. ⭐ `lc_series_comparison_matrix.json` - Matrice confronto LC-PS/PH/XP/XT
  4. ⭐ `refrigerant_compatibility_chart.json` - Tabella compatibilità refrigeranti

---

## 📊 RIEPILOGO NUMERI

### **Totale Chunks da Creare**:
- **Prodotti**: 62 chunks
  - TK1+: 4 chunks
  - TK3+ (3 versioni): 12 chunks
  - TK4/TK4 MODBUS: 16 chunks
  - LC-PS/PH/XP/XT: 14 chunks
  - K25: 3 chunks
  - Rotalock: 3 chunks
  - Adapters: 2 chunks
  - ATEX: 6 chunks (2 già creati)
  - Other: 2 chunks

- **Tecnologia**: 11 chunks
  - IR Technology: 5 chunks
  - Business Case: 3 chunks
  - Other: 3 chunks

- **Applicazioni**: 10 chunks
  - Refrigerazione: 4 chunks
  - HVAC: 3 chunks
  - Marine: 3 chunks

- **Supporto**: 13 chunks
  - Installation: 4 chunks
  - Troubleshooting: 5 chunks
  - Selection: 4 chunks

**TOTALE: ~96 chunks** (18 già creati = 78 da creare)

---

### **Totale Q&A da Creare**:
- TK Series: 43 Q&A
- LC Series: 26 Q&A
- Altri prodotti: 13 Q&A
- Tecnologia: 14 Q&A
- ATEX: 10 Q&A

**TOTALE: ~106 nuove Q&A** (30 già create)

---

## 🎯 PRIORITÀ DI CREAZIONE

### **FASE 1 - Completamento Prodotti Core (Priorità ALTA)**
1. TK3+ versioni complete (9 chunks mancanti)
2. TK4 MODBUS dettagli (7 chunks)
3. LC series completo (11 chunks)

### **FASE 2 - Tecnologia e Differenziazione (Priorità MEDIA)**
1. IR technology approfondimento (4 chunks)
2. Business case e ROI (2 chunks)
3. ATEX completo (4 chunks)

### **FASE 3 - Applicazioni e Nicchie (Priorità MEDIA-BASSA)**
1. Settori specifici (10 chunks)
2. Prodotti secondari (K25, Rotalock, Adapters - 8 chunks)

### **FASE 4 - Supporto e Servizi (Priorità BASSA)**
1. Guide installazione (4 chunks)
2. Troubleshooting avanzato (4 chunks)
3. Selection tools (2 chunks)

---

## 📝 PROSSIMI PASSI

1. **Validare questo piano** - Confermare struttura e priorità
2. **Leggere documenti fonte** - Estrarre info da MHTML/PDF
3. **Creare chunks FASE 1** - Iniziare da TK3+ e TK4 MODBUS
4. **Testare con chatbot** - Verificare qualità risposte
5. **Iterare e migliorare** - Aggiungere dettagli in base a feedback

---

**📅 Creato**: 2025-11-04  
**👤 Autore**: Teklab AI Team  
**🔄 Versione**: 1.0
