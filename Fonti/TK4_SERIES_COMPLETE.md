---
category: Oil_Level_Regulators
keywords:
- TK4 Series
- TK4 smart oil level regulator
- TK4 46 bar
- TK4 80 bar
- TK4 130 bar
- Modbus RS485
- NFC configuration
- TK4-PRG-NANO
- wireless configuration
- BMS integration
- SCADA connectivity
- remote monitoring
- smart oil management
- CO2 transcritical
- field programmable
- NFC Nano Interface
language: EN
product: TK4_Series
document_type: unified_complete
last_updated: 2025-11-15
---

# TK4 Series - Complete Product Documentation

**Smart Oil Level Regulators with Integrated Connectivity (Modbus RS485 + NFC)**

---

## 📋 Document Structure

This unified document covers the complete TK4 product family organized in the following sections:

1. **Product Family Overview** - Series description and variant comparison
2. **Variant-Specific Details** - Technical specs for each pressure variant (46/80/130 bar)
3. **Common Features** - Shared technology across all variants
4. **Connectivity Features** - Modbus RS485 and NFC configuration
5. **Technical Specifications** - Electrical, mechanical, environmental specs
6. **Applications & Selection** - Use cases and variant selection guide
7. **Installation & Service** - Mounting, wiring, configuration, maintenance
8. **FAQ** - Frequently asked questions
9. **Connectivity Features (NFC Nano Interface)** - Wireless configuration and diagnostics

---

## 1. PRODUCT FAMILY OVERVIEW

### TK4 Series Description

The **TK4 Series** is a family of smart oil level regulators combining electro-optic level detection, integrated solenoid valve, and revolutionary connectivity features (Modbus RS485 + NFC configuration). Available in three pressure variants to cover standard refrigeration through CO2 transcritical applications with BMS integration capability.

**Core Technology:**
- Electro-optic IR sensor (fused glass hermetic seal)
- Integrated NC solenoid valve
- **Modbus RS485** communication for BMS/SCADA integration
- **NFC wireless configuration** (TK4-PRG-NANO dongle via smartphone/tablet)
- Field-programmable setpoints and timings
- Automatic operation with remote monitoring
- Dual LEFT/RIGHT mounting capability
- Two-part serviceable design

**Product Family:**

| Model | Max Pressure | MOPD | Primary Applications | Connectivity |
|-------|-------------|------|---------------------|--------------|
| **TK4 46 bar** | 46 bar | 26 bar | Standard refrigeration + BMS (R134a, R404A, R407C, R410A) | Modbus + NFC |
| **TK4 80 bar** | 80 bar | 60 bar | CO2 subcritical + BMS, R410A hot climate | Modbus + NFC |
| **TK4 130 bar** | 130 bar | 100 bar | CO2 transcritical + BMS, extreme high-pressure systems | Modbus + NFC |

**Key Differentiator vs TK3+ Series:**
- **TK3+**: Basic automatic control, DIP switch configuration, no connectivity
- **TK4**: Smart control, NFC wireless config, Modbus RS485, remote monitoring, field programmable

**Selection Criteria:**
- Calculate **MOPD** (Separator Pressure - Crankcase Pressure)
- Determine if BMS integration required (TK4) or standalone sufficient (TK3+)
- Choose pressure variant with 20-30% safety margin above calculated MOPD
- Consider cost: TK4 is 50-80% more expensive than TK3+ (connectivity premium)

**Common Characteristics (All TK4 Variants):**
- Modbus RS485 for real-time monitoring and data logging
- NFC configuration (no enclosure opening, smartphone/tablet interface)
- Field-programmable setpoints, timings, alarm thresholds
- Remote diagnostics via BMS network
- Same physical mounting as TK3+ (drop-in replacement)
- Sight-glass replacement (3/4/6-hole flanges via adapters)
- IP65 enclosure protection
- CE certified (EMC + LVD)
- 20VA power consumption per unit
- Service without depressurization

---

## 2. VARIANT-SPECIFIC DETAILS

### 2.1 TK4 46 bar - Standard Pressure Smart Variant

**Overview:**
Standard pressure smart oil level regulator with Modbus RS485 and NFC configuration for conventional refrigeration systems requiring BMS integration. Most versatile variant suitable for R134a, R404A, R407C, R410A with centralized monitoring.

**Pressure Ratings:**
- Max Working Pressure: **46 bar**
- MOPD: **26 bar**
- Typical separator pressure range: 10-35 bar
- Typical crankcase pressure range: 2-10 bar

**Primary Applications:**
- Commercial refrigeration with BMS (supermarket racks, cold storage)
- Multi-compressor systems requiring centralized data collection
- Smart facilities with IoT connectivity requirements
- Predictive maintenance applications with data logging
- R410A air conditioning with remote monitoring (normal climate)
- Building management systems integration

**Connectivity Features:**
- **Modbus RS485**: Real-time oil level status, valve state, alarm conditions, operating hours
- **NFC Configuration**: Field-adjustable setpoints, timings, alarm delays via smartphone
- **Data Logging**: Historical data for predictive maintenance and optimization

**Dimensions:**
- Height: 108.25 mm
- Width (electronics): 59.5 mm
- Total width (with projections): 78 mm

**Weight:** 800-1000g (depending on adapter)

**Refrigerant Compatibility:**
- R134a, R404A, R407C, R410A (primary)
- R290, R600a (hydrocarbon)
- CO2 subcritical (ONLY if differential < 26 bar - rare)
- Ammonia (consult Teklab for approval)

**When to Choose TK4 46 bar:**
- Standard refrigeration with BMS integration required
- Remote monitoring of multiple compressors needed
- Smartphone configuration preferred (faster commissioning)
- Separator pressure < 35 bar, differential < 26 bar
- Future-proof installation (add connectivity now or later)

**Cost Consideration:**
- ~50-80% more expensive than TK3+ 46 bar
- Justified when BMS integration eliminates site visits or enables predictive maintenance

---

### 2.2 TK4 80 bar - High Pressure Smart Variant

**Overview:**
High-pressure smart oil level regulator with Modbus RS485 and NFC configuration designed for CO2 subcritical systems and high-temperature R410A applications requiring BMS integration. Reinforced components for 80 bar maximum working pressure with connectivity.

**Pressure Ratings:**
- Max Working Pressure: **80 bar**
- MOPD: **60 bar**
- Typical separator pressure range: 30-70 bar
- Typical crankcase pressure range: 5-20 bar

**Primary Applications:**
- CO2 subcritical refrigeration with BMS (40-70 bar separator pressure)
- R410A hot climate with remote monitoring (50-55°C condensing)
- High-pressure oil return systems requiring centralized monitoring
- Supermarket CO2 cascade systems with SCADA integration
- Smart CO2 facilities with predictive maintenance

**Connectivity Features:**
- **Modbus RS485**: Critical for CO2 systems requiring pressure/level monitoring
- **NFC Configuration**: Field optimization for CO2 subcritical parameters
- **Remote Diagnostics**: Troubleshoot high-pressure systems without site visits

**Dimensions:**
- Height: 107.75 mm
- Width (electronics): 59.5 mm
- Total width (with projections): 78 mm

**Weight:** 850-1050g (heavier valve body vs 46 bar)

**Refrigerant Compatibility:**
- CO2 subcritical (primary application)
- R410A hot climate (50°C+ condensing)
- All refrigerants compatible with 46 bar variant

**When to Choose TK4 80 bar:**
- CO2 subcritical systems requiring BMS integration (differential 30-60 bar)
- R410A hot climate with remote monitoring (differential > 26 bar)
- High-pressure separator (50-70 bar) with centralized data collection
- Predictive maintenance for CO2 systems (valve cycle monitoring)

**Key Difference vs TK4 46 bar:**
- Reinforced valve body and seat materials
- 80 bar rated glass dome (thicker wall)
- Higher MOPD capability (60 vs 26 bar)
- Same connectivity features (Modbus + NFC)
- ~15% higher cost than TK4 46 bar

---

### 2.3 TK4 130 bar - Very High Pressure Smart Variant

**Overview:**
Maximum pressure smart oil level regulator with Modbus RS485 and NFC configuration specifically engineered for CO2 transcritical refrigeration. Heavy-duty construction handles extreme pressures (gas cooler 80-120 bar) with full BMS integration.

**Pressure Ratings:**
- Max Working Pressure: **130 bar**
- MOPD: **100 bar**
- Typical separator pressure range: 80-120 bar (gas cooler outlet)
- Typical crankcase pressure range: 30-40 bar

**Primary Applications:**
- CO2 transcritical refrigeration systems with BMS
- CO2 heat pump applications with remote monitoring (transcritical cycle)
- Supermarket transcritical booster systems with SCADA integration
- Extreme high-pressure systems requiring centralized monitoring
- Smart CO2 transcritical facilities with predictive maintenance

**Connectivity Features:**
- **Modbus RS485**: Essential for transcritical systems (critical pressure monitoring)
- **NFC Configuration**: Field optimization for transcritical gas cooler conditions
- **Remote Diagnostics**: Critical for high-pressure safety monitoring

**Dimensions:**
- Height: 107.75 mm
- Width (electronics): 59.5 mm
- Total width (with projections): 78 mm

**Weight:** 900-1100g (heaviest valve construction)

**Refrigerant Compatibility:**
- CO2 transcritical (primary and exclusive application)
- Not typically used for HFC/HFO refrigerants (overkill)

**When to Choose TK4 130 bar:**
- CO2 transcritical ONLY with BMS integration
- Gas cooler pressure > 80 bar with remote monitoring required
- Differential pressure 60-100 bar with centralized data logging
- Safety-critical applications requiring real-time pressure alerts

**Key Difference vs TK4 80 bar:**
- Maximum reinforced valve body (heavy-duty)
- 130 bar rated glass dome (maximum thickness)
- MOPD 100 bar (highest in TK4 series)
- Same connectivity features (Modbus + NFC)
- ~25% higher cost vs TK4 80 bar

**Design Notes:**
- Over-specification for HFC systems (use TK4 46 or 80 bar instead)
- Same external dimensions as TK4 80 bar (interchangeable mounting)
- Same electronic module across all TK4 variants (pressure rating in valve/sensor only)
- Connectivity features identical across all variants

---

## 3. COMMON FEATURES (All TK4 Variants)

### 3.1 Integration & Automation

**Complete Integrated System:**
- Electro-optic sensor + solenoid valve + control + connectivity in single unit
- No external controller, wiring harnesses, or I/O modules required
- Factory tested and programmed, field reconfigurable via NFC
- Plug-and-play installation with advanced connectivity available on demand

**Automatic Operation:**
- Self-contained sensor + valve + control (operates identically to TK3+ for basic function)
- No PLC programming required for automatic oil level control
- Connectivity is optional enhancement (not required for basic operation)
- Future-proof: add Modbus later without hardware replacement

**Dual LEFT/RIGHT Mounting:**
- Same product works on either side of compressor
- Electronic module and valve body rotate to match installation side
- **50% inventory SKU reduction** (no separate left/right models)
- Installation flexibility (choose mounting side during installation)

### 3.2 Revolutionary Design Features

**Sight-Glass Replacement:**
- Direct mounting to 3/4/6-hole compressor flanges (via Teklab adapters)
- Maintains visual inspection capability (LED indication replaces glass viewing)
- Combines visual + automatic electronic control + connectivity
- Eliminates separate sight-glass + sensor + connectivity installations

**Two-Part Modular Design:**
- **Part 1** (permanent): Sensor adapter + valve body
  - Remains on compressor during service
  - Brazed/flanged connections intact
- **Part 2** (replaceable): Electronic module + connectivity board
  - 5-10 minute replacement time
  - No system depressurization required
  - No refrigerant recovery
  - Pre-configure module via NFC before installation

### 3.3 Detection & Control Technology

**Electro-Optic Level Sensor:**
- Infrared detection through fused glass dome
- Detection principle: refractive index change (oil vs air/refrigerant vapor)
- **No moving parts** (no float mechanism, no reed switch)
- Response time: **< 1 second**
- Factory calibrated (no field adjustment needed)
- MTTF: **> 100,000 hours** (11+ years continuous)

**Fused Glass Hermetic Seal:**
- Glass-to-metal molecular fusion (NOT O-ring sealed)
- Zero leakage rating: 10^-12 mbar·L/s (true hermetic)
- Chemically inert to all oils and refrigerants
- Lifetime seal (no maintenance, no degradation)
- Pressure rated per variant (46/80/130 bar glass thickness)

**Sensor Advantages:**
- No wetted electronics (sensor isolated from media)
- No contamination from oil/refrigerant
- Works with all oil types (mineral, POE, PAG, AB)
- Immune to foam, bubbles (infrared detection)
- Self-diagnostic LED indication + Modbus status reporting

### 3.4 Electrical Features

**Power Supply:**
- **24VAC ±10%** or **230VAC ±10%** (model dependent - specify at order)
- Power consumption: **20VA per unit** (includes sensor + valve + connectivity)
- Frequency: 50/60 Hz

**Alarm Relay Output:**
- Rating: **230VAC @ 2A** (high power)
- Contacts: NO + NC (configurable)
- Typical use: NC contact in series with compressor contactor (safety chain)
- Direct safety chain integration (no intermediate relay needed)

**Electrical Connection Options:**
- EN175301-803 connectors (9.4mm): 3m or 6m cable length
- Cable glands (M12 or M16): 1 meter cable length
- Cable type: PVC CEI 20-22 (-20°C to +70°C rated)

**Multi-Compressor Power Requirements:**

| Compressors | Total Power | Recommended Transformer |
|-------------|-------------|-------------------------|
| 1 unit | 20VA | 30VA minimum |
| 2 units | 40VA | 60VA minimum |
| 3 units | 60VA | 100VA minimum |
| 4 units | 80VA | 120VA minimum |
| 6 units | 120VA | 150VA minimum |

*Note: Size transformer 50-60% above total load for inrush current and margin.*

### 3.5 Installation & Reliability

**Reduced Leak Points:**
- TK4 system: **2 junctions** (flange + oil inlet)
- Separate components: **6+ junctions** (sensor flange, valve inlet/outlet, piping)
- Fewer leak points = higher system reliability

**Simplified Wiring:**
- TK4: **6-8 wires total** (2 power + 2 relay + 2-4 Modbus RS485)
- Separate sensor + valve + controller: **12+ wires**

**Compact Dimensions:**
- Height: 107-108mm (depending on variant)
- Width (electronics): 59.5mm
- Total width (with projections): 78mm
- Comparable to traditional sight-glass

**IP65 Enclosure Protection:**
- Dust-tight (complete protection from dust ingress)
- Water jet protected (12.5 L/min from any angle)
- Suitable for outdoor installations
- Temperature range: -40°C to +60°C ambient

**Service Access:**
- Electronic module (including connectivity board) replaceable without system depressurizing
- Module secured with screws (no special tools)
- Disconnect power → remove screws → lift module → replace
- 5-10 minute service time vs hours for valve replacement

---

## 4. CONNECTIVITY FEATURES

### 4.1 Modbus RS485 Communication

**Protocol & Specifications:**
- **Protocol**: Modbus RTU (industry standard)
- **Physical**: RS485 twisted pair (2-wire, daisy-chain topology)
- **Baud Rates**: 9600, 19200, 38400 bps (NFC configurable)
- **Data Format**: 8N1, 8E1, 8O1 (NFC configurable)
- **Address Range**: 1-247 (NFC configurable, unique per device)
- **Max Distance**: 1200m (twisted pair cable)
- **Termination**: 120Ω resistors at both ends of network

**Real-Time Monitoring Data:**
- Oil level status (OK / LOW / ALARM)
- Valve state (OPEN / CLOSED)
- Alarm status and history
- Operating hours (valve and sensor)
- Valve cycle counter (predictive maintenance)
- Module temperature
- Configuration parameters (read-only)

**BMS Integration Benefits:**
- Centralized monitoring of multiple compressors
- Historical data logging for trend analysis
- Predictive maintenance (valve cycle tracking)
- Remote diagnostics (troubleshoot without site visits)
- Alarm forwarding to BMS/SCADA systems
- Energy optimization (oil return pattern analysis)

**Typical Polling Rate:**
- 1-5 seconds per TK4 unit (depends on BMS configuration)
- Faster polling for critical applications (CO2 transcritical)
- Slower polling for energy conservation

### 4.2 NFC Wireless Configuration

**Technology:**
- **Standard**: ISO/IEC 14443 Type A
- **Frequency**: 13.56 MHz
- **Range**: 0-40mm proximity (hold device near TK4 housing)
- **Security**: Password-protected access
- **Interface**: Smartphone/tablet app + TK4-PRG-NANO USB dongle

**Configuration Process:**
1. Download Teklab App (iOS/Android)
2. Connect TK4-PRG-NANO dongle to smartphone/tablet
3. Hold device near TK4 housing (no enclosure opening needed)
4. Enter password (default in manual, changeable)
5. Adjust parameters (see below)
6. Save configuration (takes 2-5 seconds)

**Configurable Parameters:**
- **Oil Level Setpoints**: Adjust fill/stop levels to match compressor requirements
- **Valve Timings**: Opening/closing delays for optimization
- **Alarm Delays**: Configure alarm activation delay (60-180 sec) to prevent nuisance alarms
- **Modbus Settings**: Address (1-247), baud rate, data format
- **Display Language**: Multi-language options
- **Password**: Change default password for security

**NFC Advantages:**
- **No panel opening** (configure through enclosure, IP65 maintained)
- **No cable connection** (wireless, faster than USB configuration)
- **Field flexibility** (adjust setpoints without controller replacement)
- **Backup/Restore** (save configuration profiles for multiple units)
- **Faster commissioning** (configure multiple units in minutes)

**Security Features:**
- Password-protected access (prevents unauthorized changes)
- Modbus read-only for configuration (prevents BMS software errors)
- NFC-only write access (technician must be on-site)

### 4.3 Configuration Comparison

**TK3+ (DIP Switches):**
- Manual on-site parameter adjustment
- Requires panel access (IP65 compromised during config)
- Limited parameters (basic setpoints only)
- Time-consuming for multiple units

**TK4 (NFC Wireless):**
- Smartphone/tablet wireless configuration
- No panel opening (IP65 maintained)
- Full parameter access (setpoints, timings, Modbus, alarms)
- Fast commissioning (configure multiple units in minutes)

**When NFC Configuration Essential:**
- Multiple compressor installations (commissioning speed)
- Parameter optimization during startup (trial-and-error adjustments)
- Future flexibility (no controller replacement for setpoint changes)
- Harsh environments (minimize enclosure openings, IP65 integrity)

---

## 5. TECHNICAL SPECIFICATIONS

### 5.1 Electrical Specifications (Common to All Variants)

| Parameter | Specification |
|-----------|--------------|
| Supply Voltage | 24VAC ±10% or 230VAC ±10% (model dependent) |
| Supply Current | 20VA per unit (sensor + valve + connectivity) |
| Electrical Connection | 9.4mm EN175301-803 connectors OR M12/M16 cable glands |
| Output Signal | Contact-free relay (NO + NC) |
| Relay Rating | 230VAC @ 2A resistive |
| Cable Type | PVC CEI 20-22 rated -20°C to +70°C |
| Cable Lengths | 1m (glands), 3m or 6m (connectors) |
| Frequency | 50/60 Hz |

### 5.2 Connectivity Specifications

| Feature | Modbus RS485 | NFC Interface |
|---------|--------------|---------------|
| Protocol | Modbus RTU | ISO/IEC 14443 Type A |
| Physical Layer | RS485 twisted pair | 13.56 MHz RFID |
| Baud Rates | 9600, 19200, 38400 bps | - |
| Data Format | 8N1, 8E1, 8O1 | - |
| Address Range | 1-247 | - |
| Max Distance | 1200m (twisted pair) | 0-40mm proximity |
| Termination | 120Ω at endpoints | - |
| Security | - | Password-protected |
| Configuration | NFC only (write access) | Read/write |
| Monitoring | Read-only (BMS polling) | Read-only |

### 5.3 Mechanical Specifications (Variant-Specific)

| Parameter | TK4 46 bar | TK4 80 bar | TK4 130 bar |
|-----------|------------|------------|-------------|
| Housing Material | Nickel-plated steel + fused glass (sensor) | Same | Same |
| Electronics Housing | PA glass fiber reinforced + connectivity board | Same | Same |
| Enclosure Protection | IP65 | IP65 | IP65 |
| Flange Connection | 3/4/6-hole (via adapters) | Same | Same |
| Oil Return Line | 7/16-20 UNF male | Same | Same |
| Height (mm) | 108.25 | 107.75 | 107.75 |
| Width Electronics (mm) | 59.5 | 59.5 | 59.5 |
| Total Width (mm) | 78 | 78 | 78 |
| Weight (g) | 800-1000 | 850-1050 | 900-1100 |
| Module Weight (g) | 150-200 (replaceable) | 150-200 | 150-200 |

### 5.4 Environmental & Pressure Specifications

| Parameter | TK4 46 bar | TK4 80 bar | TK4 130 bar |
|-----------|------------|------------|-------------|
| Media Temperature | -40°C to +85°C | -40°C to +85°C | -40°C to +85°C |
| Ambient Temperature | -40°C to +60°C | -40°C to +60°C | -40°C to +60°C |
| Max Working Pressure | **46 bar** | **80 bar** | **130 bar** |
| MOPD (Max Differential) | **26 bar** | **60 bar** | **100 bar** |
| Humidity | 5-95% RH non-condensing | 5-95% RH non-condensing | 5-95% RH non-condensing |
| Vibration | IEC 60068-2-6 compliant | IEC 60068-2-6 compliant | IEC 60068-2-6 compliant |

### 5.5 Sensor Specifications (Common to All Variants)

| Parameter | Specification |
|-----------|--------------|
| Sensor Type | Electro-optic (infrared refractive index) |
| Detection Method | Oil/air interface via refractive index change |
| Response Time | < 1 second |
| Moving Parts | Zero (solid-state) |
| Calibration | Factory calibrated (no field adjustment) |
| MTTF | > 100,000 hours (11+ years) |
| Repeatability | ± 1mm |
| Hermetic Seal | Fused glass-to-metal (10^-12 mbar·L/s) |

### 5.6 Valve Specifications (Variant-Specific)

| Parameter | TK4 46 bar | TK4 80 bar | TK4 130 bar |
|-----------|------------|------------|-------------|
| Valve Type | NC (Normally Closed) solenoid | Same | Same |
| Operation | Automatic (sensor-controlled) | Same | Same |
| Pressure Rating | 46 bar max, MOPD 26 bar | 80 bar max, MOPD 60 bar | 130 bar max, MOPD 100 bar |
| Serviceable Coil | Yes (no depressurization) | Yes | Yes |
| Valve Body Material | Nickel-plated steel | Reinforced steel | Heavy-duty steel |
| Response Time | < 2 seconds (open/close) | < 2 seconds | < 2 seconds |

### 5.7 Compliance (All Variants)

| Standard | Description |
|----------|-------------|
| 2014/30/UE | EMC Directive (Electromagnetic Compatibility) |
| 2014/35/UE | Low Voltage Directive |
| CE Marking | Compliant and certified |
| IP Rating | IP65 (dust-tight, water jet protected) |
| Modbus | Modbus RTU compliant |
| NFC | ISO/IEC 14443 Type A |

### 5.8 Refrigerant & Oil Compatibility

**Refrigerants:**

| Variant | Compatible Refrigerants |
|---------|------------------------|
| TK4 46 bar | R134a, R404A, R407C, R410A, R290, R600a, CO2 subcritical (if MOPD < 26 bar), Ammonia (approval required) |
| TK4 80 bar | CO2 subcritical, R410A hot climate, all 46 bar refrigerants |
| TK4 130 bar | CO2 transcritical (primary), all other refrigerants (overkill for HFC) |

**Oils:**
All variants compatible with: Mineral, POE, PAG, AB, PVE, and all synthetic oils (fused glass + nickel-plated steel = universal compatibility)

---

## 6. APPLICATIONS & SELECTION GUIDE

### 6.1 Application Examples by Variant

#### TK4 46 bar Applications

**Commercial Refrigeration with BMS:**
- Supermarket rack systems with centralized monitoring (R404A, R134a)
- Multi-store chain facilities (remote monitoring, predictive maintenance)
- Cold storage warehouses with SCADA integration
- Smart facilities requiring IoT connectivity

**Industrial Refrigeration with Remote Monitoring:**
- Food processing plants (centralized data logging)
- Pharmaceutical storage (compliance documentation via Modbus)
- Brewery and beverage cooling (predictive maintenance)

**Building Management Systems:**
- Chiller plants with BMS integration (R134a, R407C)
- Rooftop units with remote monitoring (R410A)
- Process cooling with centralized control

**Multi-Compressor Systems:**
- Parallel rack systems (3-6 compressors with centralized monitoring)
- Automatic oil equalization with data logging
- Predictive maintenance via valve cycle tracking

#### TK4 80 bar Applications

**CO2 Subcritical Systems with BMS:**
- Supermarket CO2 cascade systems (MT stage monitoring)
- Industrial CO2 refrigeration with SCADA (40-70 bar)
- CO2 booster systems with remote diagnostics

**High-Pressure HFC Systems with Monitoring:**
- R410A hot climate with remote alerts (50-55°C condensing)
- High-pressure oil separators requiring monitoring (50-70 bar)
- Industrial systems with BMS integration

**Extreme Differential Applications:**
- High separator pressure + low suction with centralized monitoring
- Systems with 30-60 bar differential requiring data logging
- Safety-critical applications with real-time pressure alerts

#### TK4 130 bar Applications

**CO2 Transcritical Systems with BMS:**
- Supermarket transcritical CO2 systems with SCADA
- Gas cooler outlet 80-120 bar with remote monitoring
- CO2 heat pumps with predictive maintenance (transcritical cycle)

**Extreme High-Pressure with Remote Monitoring:**
- Industrial CO2 transcritical with centralized control
- Applications above 80 bar requiring real-time monitoring
- Differential pressure 60-100 bar with BMS integration

### 6.2 Variant Selection Process

**Step 1: Determine Connectivity Requirement**
- **BMS/SCADA integration required?** → TK4 series (Modbus RS485)
- **Remote monitoring needed?** → TK4 series
- **Predictive maintenance desired?** → TK4 series (valve cycle tracking)
- **Basic automatic control sufficient?** → TK3+ series (50-80% less expensive)

**Step 2: Calculate MOPD**
```
MOPD = Separator Pressure (bar) - Crankcase Pressure (bar)
```

**Step 3: Add Safety Margin**
```
Required MOPD Rating = Calculated MOPD × 1.2-1.3
```

**Step 4: Select Variant**

| Calculated MOPD | Required Rating | Recommended Variant |
|----------------|----------------|---------------------|
| 0-20 bar | 24-26 bar | **TK4 46 bar** |
| 20-50 bar | 24-60 bar | **TK4 80 bar** |
| 50-80 bar | 60-100 bar | **TK4 130 bar** |
| > 80 bar | > 96 bar | **TK4 130 bar** (maximum) |

**Step 5: Verify Application Match**
- CO2 transcritical → TK4 130 bar (mandatory)
- CO2 subcritical → TK4 80 bar or 130 bar (depending on MOPD)
- R410A hot climate → TK4 80 bar (safety margin)
- Standard HFC with BMS → TK4 46 bar

### 6.3 Selection Examples

**Example 1: R404A Supermarket Rack with BMS**
- Separator pressure: 28 bar
- Crankcase pressure: 4 bar
- MOPD: 28 - 4 = 24 bar
- Safety margin: 24 × 1.2 = 28.8 bar
- BMS integration: Required (Modbus RS485)
- **Selection: TK4 46 bar** → Acceptable, consider TK4 80 bar for better margin

**Example 2: CO2 Subcritical System with SCADA**
- Separator pressure: 60 bar
- Crankcase pressure: 15 bar
- MOPD: 60 - 15 = 45 bar
- Safety margin: 45 × 1.2 = 54 bar
- BMS integration: Required (remote monitoring)
- **Selection: TK4 80 bar (MOPD 60 bar)** → Perfect match

**Example 3: CO2 Transcritical System with BMS**
- Gas cooler outlet: 100 bar
- Crankcase pressure: 35 bar
- MOPD: 100 - 35 = 65 bar
- Safety margin: 65 × 1.2 = 78 bar
- BMS integration: Required (critical monitoring)
- **Selection: TK4 130 bar (MOPD 100 bar)** → Only option, ideal

**Example 4: R410A Standard Climate with BMS**
- Separator pressure: 25 bar (40°C condensing)
- Crankcase pressure: 8 bar
- MOPD: 25 - 8 = 17 bar
- BMS integration: Desired (facility management)
- **Selection: TK4 46 bar** → Ideal smart choice

**Example 5: R134a Chiller Plant (No BMS)**
- Separator pressure: 20 bar
- Crankcase pressure: 5 bar
- MOPD: 20 - 5 = 15 bar
- BMS integration: Not required
- **Selection: TK3+ 46 bar** → Cost-optimized (TK4 connectivity not needed)

### 6.4 TK4 vs TK3+ Decision Matrix

| Requirement | TK3+ Series | TK4 Series |
|------------|-------------|------------|
| **Automatic oil control** | ✅ Yes | ✅ Yes |
| **BMS/SCADA integration** | ❌ No | ✅ Yes (Modbus RS485) |
| **Remote monitoring** | ❌ No | ✅ Yes |
| **Smartphone configuration** | ❌ No (DIP switches) | ✅ Yes (NFC wireless) |
| **Field-programmable setpoints** | ⚠️ Limited (DIP switches) | ✅ Full (NFC) |
| **Data logging** | ❌ No | ✅ Yes (via BMS) |
| **Predictive maintenance** | ❌ No | ✅ Yes (valve cycle tracking) |
| **Cost** | Lower (50-80% less) | Higher (connectivity premium) |
| **Recommended when** | Basic automatic control | BMS integration, remote monitoring |

---

## 7. INSTALLATION & SERVICE

### 7.1 Mounting Requirements

**Clearances:**
- **Above**: 120-150mm (for electronic module removal during service)
- **Sides**: 80mm (for cable/piping access, wiring, NFC configuration)
- **Below**: 30mm minimum (glass dome immersion depth)

**Flange Adapters:**
- Adapters sold separately (not included with TK4)
- Select adapter matching compressor flange type:
  - 3-hole sight-glass flange
  - 4-hole sight-glass flange
  - 6-hole sight-glass flange
- See Teklab Adapters Addendum for selection guide
- Same adapters as TK3+ series (interchangeable)

**Orientation:**
- Vertical mounting (electronic module on top)
- Glass dome immersed in oil sump
- Dual LEFT/RIGHT capability (choose during installation)

**Oil Return Line:**
- 7/16-20 UNF male connection on valve body
- Connect to high-pressure oil separator
- Line sizing per system design (typically 1/4" OD copper)
- Install manual shutoff valve for service isolation

### 7.2 Electrical Installation

**Power Supply Wiring:**
- Use 0.75-1.5 mm² wire (18-14 AWG)
- Observe polarity for 24VAC models (if DC coil variant)
- 230VAC models: L + N (no PE connection to sensor)
- Fuse protection: 1A slow-blow per TK4 unit

**Relay Wiring (Safety Chain):**
- Use NC contact in series with compressor contactor coil
- Wire gauge: 1.0-1.5 mm² (18-14 AWG) for 230VAC @ 2A
- NC contact: Closed during normal operation → Opens on alarm
- Typical wiring: NC contact interrupts compressor contactor supply

**Modbus RS485 Wiring:**
- Use twisted pair cable (Belden 3105A or equivalent)
- Wire gauge: 0.5-0.75 mm² (22-18 AWG)
- Daisy-chain topology (not star)
- Polarity: A+ and B- (mark cables to avoid reversal)
- Install 120Ω termination resistors at both ends of network
- Maximum cable length: 1200m
- Maximum devices per network: 32 (without repeaters)

**Multi-Compressor Systems:**
- Wire all TK4 relay NC contacts in **series** (safety chain)
- Any unit alarm → stops all compressors
- Modbus network: Daisy-chain all TK4 units to BMS master
- Assign unique Modbus address to each TK4 (1-247)

### 7.3 Modbus RS485 Network Setup

**Physical Wiring:**
1. Connect twisted pair from BMS master to first TK4 (A+, B-)
2. Daisy-chain from first TK4 to second TK4 (continue for all units)
3. Install 120Ω terminator at BMS master
4. Install 120Ω terminator at last TK4 in chain
5. Verify polarity (A+ to A+, B- to B-)

**NFC Configuration for Modbus:**
1. Download Teklab App and connect TK4-PRG-NANO dongle
2. Hold smartphone near first TK4 housing
3. Configure Modbus parameters:
   - Address: 1 (unique per device)
   - Baud rate: 9600 bps (typical)
   - Data format: 8N1
4. Save configuration
5. Repeat for each TK4 (increment address: 2, 3, 4, etc.)

**BMS Master Configuration:**
1. Add Modbus devices (TK4 addresses 1-N)
2. Import TK4 register map (available from Teklab)
3. Configure polling rate (1-5 seconds per device)
4. Test communication (verify each TK4 responds)

### 7.4 NFC Configuration

**Requirements:**
- Teklab App (download from iOS App Store or Google Play)
- TK4-PRG-NANO USB dongle (order separately from Teklab)
- Smartphone or tablet (iOS/Android)

**Configuration Steps:**
1. Launch Teklab App and connect TK4-PRG-NANO dongle to device
2. Hold smartphone near TK4 housing (0-40mm range, no enclosure opening)
3. Enter password (default in manual, changeable for security)
4. Adjust parameters:
   - **Oil Level Setpoints**: Fill/stop levels (match compressor requirements)
   - **Valve Timings**: Opening/closing delays (optimization)
   - **Alarm Delays**: Delay before alarm activation (60-180 sec, prevent nuisance)
   - **Modbus Settings**: Address (1-247), baud rate, data format
   - **Display Language**: Multi-language options
5. Save configuration (takes 2-5 seconds)
6. Verify settings (read back configuration)

**Configuration Backup/Restore:**
- Save configuration profile in app (backup for multiple units)
- Clone configuration to other TK4 units (fast commissioning)
- Restore factory defaults if needed

### 7.5 Commissioning

**Pre-Startup Checklist:**
1. Verify power supply voltage matches TK4 rating (24VAC or 230VAC)
2. Check all electrical connections secure (power, relay, Modbus)
3. Verify oil return line connected and isolation valve open
4. Confirm relay wiring correct (NC contact in series with contactor)
5. Verify adequate oil in separator
6. Verify Modbus RS485 termination resistors installed (both ends)
7. Test Modbus communication (BMS master can read each TK4 address)

**Initial Startup:**
1. Power on TK4 units
2. Observe LED indication (should show red initially if crankcase empty)
3. Verify BMS master can read Modbus data (oil level status, valve state)
4. Start compressor system
5. TK4 valve opens automatically (yellow LED, valve state OPEN in BMS)
6. Oil fills crankcase to setpoint
7. TK4 valve closes (green LED, valve state CLOSED in BMS)
8. Monitor for 30 minutes to verify stable operation
9. Log Modbus data for baseline (operating hours, valve cycles)

**LED Indication:**
- **Green**: Normal operation (oil level adequate, valve closed)
- **Yellow**: Filling mode (oil level low, valve open, oil flowing)
- **Red**: Alarm (oil level low despite valve open for 60-120 sec)

### 7.6 Service & Maintenance

**Routine Maintenance:**
- **Quarterly**: Visual inspection (check for leaks, verify LED indication, review Modbus data)
- **Annually**: Functional test (verify valve operation, relay output, Modbus communication)
- **No scheduled component replacement** (replace only if failed)

**Remote Monitoring via Modbus:**
- Monitor valve cycle counter (predictive maintenance)
- Track operating hours (sensor and valve)
- Analyze alarm history (troubleshoot recurring issues)
- Detect anomalies early (valve opening frequency changes)

**Electronic Module Replacement (5-10 minutes, no depressurization):**
1. Disconnect power (lockout/tagout)
2. Remove mounting screws (typically 2-4 screws)
3. Lift electronic module straight up (disconnect internal connector)
4. Install new module (align connector, press down gently)
5. Secure with mounting screws
6. Reconnect power and verify operation
7. Reconfigure via NFC if needed (settings may be lost)
8. Verify Modbus communication restored

**Valve Coil Replacement (5-10 minutes, no depressurization):**
1. Disconnect power
2. Remove coil retaining clip or screws
3. Slide coil off valve stem
4. Install new coil (align with valve stem)
5. Secure retaining hardware
6. Reconnect power and verify operation

**Complete Sensor/Valve Body Replacement (requires depressurization):**
1. Isolate compressor and oil return line
2. Recover refrigerant from crankcase (if necessary)
3. Remove electronic module
4. Disconnect flange bolts
5. Remove sensor/valve assembly
6. Install new assembly with new gasket/O-ring
7. Reconnect oil return line
8. Reinstall electronic module
9. Reconfigure via NFC (Modbus address, setpoints)
10. Evacuate and test for leaks
11. Return to service
12. Verify Modbus communication

### 7.7 Troubleshooting

**Alarm Activates Immediately After Startup:**
- **Cause**: Oil separator empty or pressure too low
- **Solution**: Verify separator oil level, check separator pressure adequate (> 5 bar above crankcase)
- **Modbus Check**: Read valve state (should be OPEN if level low)

**Valve Won't Open (Red LED, no oil flow):**
- **Cause**: Coil failure, wiring issue, insufficient differential pressure
- **Solution**: Check power supply, verify coil voltage, measure MOPD (need > 5 bar minimum)
- **Modbus Check**: Read valve state (should show OPEN command, verify coil energized)

**Continuous Filling (Yellow LED stays on):**
- **Cause**: Oil return line restricted, valve stuck open
- **Solution**: Check for blockage, verify line sizing adequate, inspect valve seat
- **Modbus Check**: Read valve cycle counter (abnormal cycle frequency indicates issue)

**False Alarms (Intermittent Red LED):**
- **Cause**: Foam in crankcase, low refrigerant charge, undersized oil separator
- **Solution**: Check refrigerant charge, verify separator size adequate, check for liquid slugging
- **Modbus Check**: Review alarm history (pattern analysis for root cause)

**No LED Indication:**
- **Cause**: Power supply failure, electronic module failure
- **Solution**: Verify power supply voltage at terminals, check fuse, replace module if needed
- **Modbus Check**: Verify BMS cannot communicate (confirms module failure vs sensor failure)

**Modbus Communication Failure:**
- **Cause**: Wiring issue, termination missing, address conflict, wrong baud rate
- **Solution**: Check twisted pair continuity, verify 120Ω terminators installed, verify unique addresses, verify baud rate matches BMS
- **NFC Check**: Read Modbus settings (verify address, baud rate correct)

**NFC Configuration Not Working:**
- **Cause**: Distance too far (> 40mm), wrong password, dongle connection issue
- **Solution**: Hold device closer to housing, verify password correct, check dongle USB connection
- **Fallback**: Factory reset via DIP switch (if available, check manual)

---

## 8. FREQUENTLY ASKED QUESTIONS (FAQ)

### 8.1 Product Classification & Comparison

**Q1: What is the main difference between TK4 and TK3+?**

**Main difference: Configuration method**
- **TK3+**: DIP switches on device (manual parameter adjustment, panel access required)
- **TK4**: NFC wireless configuration via smartphone app (no panel opening)

**Additional TK4 features:**
- Modbus RS485 for BMS/SCADA integration
- Remote monitoring and data logging
- Field-programmable setpoints and timings

**What's identical:**
- Same IR optical sensor technology
- Same pressure ratings (46/80/130 bar)
- Same automatic valve and installation
- Same refrigerant compatibility

**Choose TK3+ when**: Basic automatic control sufficient, no BMS integration needed, cost priority (50-80% less expensive)

**Choose TK4 when**: BMS/SCADA integration required, NFC smartphone config preferred, remote monitoring needed

**Q2: Is TK4 a regulator or level switch?**
TK4 is a complete **oil level regulator** (not just a level switch). It combines electro-optic level detection with integrated solenoid valve and control electronics for automatic oil level regulation. Connectivity adds monitoring capability but does not change core function.

**Q3: TK4 vs TK1+ - What's the difference?**
- **TK4** = Oil level **regulator** (sensor + valve + control + connectivity integrated, automatic operation)
- **TK1+** = Level **switch** (detection only, requires separate valve and external controller)

Use TK4 for automatic plug-and-play operation with BMS integration. Use TK1+ for custom PLC control systems.

### 8.2 Connectivity & Configuration

**Q4: How do I configure TK4 with NFC?**
1. Download Teklab App (iOS/Android) and obtain TK4-PRG-NANO USB dongle
2. Connect dongle to smartphone/tablet
3. Hold device near TK4 housing (0-40mm NFC range, no enclosure opening)
4. Enter password (default in manual)
5. Adjust parameters: oil level setpoint, Modbus address, baud rate, alarm delays
6. Save configuration (takes 2-5 seconds)

**No enclosure opening or cable connections required.**

**Q5: How do I set up Modbus RS485?**

**Wiring:**
- Connect twisted pair to RS485 terminals (A+, B-)
- Daisy-chain multiple units
- Install 120Ω terminators at both ends
- Max 1200m cable length

**Configuration via NFC:**
- Assign unique Modbus address (1-247)
- Set baud rate (9600/19200/38400 bps)
- Choose format (8N1/8E1/8O1)

**BMS Integration:**
- Configure master with TK4 addresses
- Import register map
- Poll for oil level status/valve state/alarms/operating hours

**Q6: What data can I read via Modbus?**
- Oil level status (OK / LOW / ALARM)
- Valve state (OPEN / CLOSED)
- Alarm status and history
- Operating hours (sensor and valve)
- Valve cycle counter (predictive maintenance)
- Module temperature
- Configuration parameters (read-only)

Typical polling rate: 1-5 seconds per unit.

**Q7: Can I adjust setpoints remotely via Modbus?**
No. Setpoint adjustment **only via NFC** (security feature):
- Modbus: Read-only access to configuration
- NFC: Read/write with password protection
- Prevents accidental parameter changes via BMS software errors

Technician must visit site with smartphone/tablet for setpoint changes.

**Q8: Can I use TK4 without Modbus or NFC?**
Yes. TK4 works standalone:
- Leave RS485 terminals unconnected if Modbus not needed
- Factory default settings work for most applications
- Future-proof: add connectivity later without hardware replacement

**If connectivity never needed, TK3+ more cost-effective.**

### 8.3 Operation & Installation

**Q9: Does TK4 require external controllers?**
No. TK4 operates automatically out-of-box (plug-and-play):
- Factory programmed for immediate operation
- Self-contained sensor + valve + control
- Modbus/NFC are optional enhancements (not required for basic operation)
- Operates identically to TK3+ for automatic oil level control

**Q10: What adapters are compatible with TK4?**
TK4 uses same adapters as TK3+ series:
- Bitzer, Copeland, Frascold, Dorin, Bock compressor adapters
- 3-hole, 4-hole, 6-hole flange adapters
- Sight-glass replacement mounting

Order adapters separately. Specify compressor brand/model when ordering.

**Q11: Can TK4 replace existing TK3+ units?**
Yes, drop-in replacement:
- Identical dimensions (108.25mm H × 59.5mm W)
- Same adapters, flanges, voltage options (24VAC/230VAC)
- Same power consumption (20VA)
- Retrofit: Remove TK3+, install TK4 on existing adapter, add Modbus wiring (optional)

### 8.4 Pressure & Applications

**Q12: What does MOPD mean?**
MOPD = **Maximum Operating Pressure Differential** (separator pressure minus crankcase pressure).

**TK4 Variants:**
- TK4 46 bar: MOPD 26 bar
- TK4 80 bar: MOPD 60 bar
- TK4 130 bar: MOPD 100 bar

**Calculation:** Separator pressure - Crankcase pressure ≤ MOPD rating

**Example:** 28 bar separator - 3 bar crankcase = 25 bar differential (OK for TK4 46 bar)

**Q13: Which TK4 variant for CO2 systems?**
- **CO2 subcritical** (differential 30-60 bar): TK4 80 bar
- **CO2 transcritical** (differential 60-100 bar): TK4 130 bar

**Note:** CO2 systems typically require BMS integration (TK4 ideal choice).

**Q14: Can TK4 46 bar be used for CO2?**
No, CO2 exceeds MOPD 26 bar:
- CO2 subcritical: 40-60 bar differential → Use TK4 80 bar
- CO2 transcritical: 70-100 bar differential → Use TK4 130 bar

**TK4 46 bar suitable for**: R134a, R404A, R407C, R410A (standard conditions), all systems with differential < 26 bar.

**Q15: R410A hot climate - which TK4 model?**
R410A at 50°C condensing creates ~30 bar differential. Use **TK4 80 bar** for safety margin (MOPD 60 bar). TK4 46 bar works but operates at maximum rating (less safe).

### 8.5 Service & Troubleshooting

**Q16: How do I replace the TK4 module?**
1. Disconnect power
2. Remove mounting screws
3. Lift off module
4. Install new module
5. Reconnect power
6. Reconfigure via NFC if needed

**Time:** 5-10 minutes, no refrigerant recovery needed.

**Q17: What maintenance is required?**
- **Quarterly**: Visual inspection, review Modbus data (valve cycles, alarms)
- **Annually**: Functional test (verify valve operation, relay output, communication)
- **No scheduled component replacement** (only replace if failed)

**Predictive maintenance via Modbus**: Monitor valve cycle counter for early failure detection.

**Q18: How to troubleshoot Modbus communication failure?**
- Check twisted pair continuity
- Verify 120Ω terminators installed at both ends
- Verify unique Modbus addresses (no conflicts)
- Verify baud rate matches BMS master
- Use NFC to read/verify Modbus settings

**Q19: NFC configuration not working - what to check?**
- Distance too far (must be < 40mm from housing)
- Wrong password (verify default or changed password)
- Dongle connection issue (check USB connection)
- Try factory reset (if available, check manual)

**Q20: Can I upgrade TK3+ to TK4 connectivity?**
No. Hardware is different (TK4 has connectivity board integrated). However:
- Same mounting footprint (drop-in replacement)
- Same adapters compatible
- Retrofit process: Remove TK3+, install TK4, add Modbus wiring

---

## 9. ORDERING INFORMATION

### 9.1 Product Code Structure

**Format**: `TK4-[Pressure]-[Voltage]-[Cable Type]-[Cable Length]`

**Example**: `TK4-46-230VAC-CON-3M`
- TK4 series (smart connectivity)
- 46 bar max pressure variant
- 230VAC power supply
- Connector type (EN175301-803)
- 3 meter cable length

### 9.2 Selection Options

**Pressure Variant:**
- `46` = TK4 46 bar (MOPD 26 bar)
- `80` = TK4 80 bar (MOPD 60 bar)
- `130` = TK4 130 bar (MOPD 100 bar)

**Power Supply Voltage:**
- `24VAC` = 24VAC ±10%
- `230VAC` = 230VAC ±10%

**Cable Type:**
- `GLAND` = Cable glands (M12 or M16)
- `CON` = EN175301-803 connectors (9.4mm)

**Cable Length:**
- `1M` = 1 meter (glands only)
- `3M` = 3 meters (connectors only)
- `6M` = 6 meters (connectors only)

### 9.3 Accessories (Sold Separately)

**Required:**
- **Adapter**: TK4 requires an adapter to mount to compressor flange (3/4/6-hole types). See Teklab Adapters Addendum.

**Optional:**
- **TK4-PRG-NANO**: NFC configuration dongle (USB, iOS/Android compatible)
- **Teklab App**: Download free from App Store or Google Play

---

## Document Information

**Document**: TK4 Series Complete Product Documentation  
**Version**: 1.0  
**Date**: 2025-11-12  
---

## 9. CONNECTIVITY FEATURES (NFC NANO INTERFACE)

### 9.1 Nano Interface Overview

The **Nano Interface** is TK4's revolutionary wireless near-field communication (NFC) system that enables direct interaction with the oil level regulator using Windows PC or Android devices (smartphones/tablets) **without opening the enclosure or connecting cables**.

#### Key Innovation

**Traditional Configuration** (TK3+):
- Open enclosure
- Access DIP switches with screwdriver
- Manual potentiometer adjustment
- Close enclosure and test
- Repeat if settings incorrect

**TK4 Nano Interface** (Wireless):
- Approach unit with smartphone/tablet + USB dongle (5-10cm proximity)
- Launch App, connect wirelessly
- View/modify all parameters in real-time
- Save configuration
- No enclosure opening, no tools required

#### Hardware: TK4-PRG-NANO USB Dongle

**Physical Characteristics**:
- **USB interface**: Connects to Windows PC or Android device (USB OTG)
- **NFC transceiver**: Wireless communication to TK4 unit
- **LED indicator**: Connection status and activity
- **Compact design**: Portable, fits in pocket or toolbox
- **Operating range**: Typically 5-10cm proximity to TK4 housing
- **One dongle**: Configure unlimited TK4 units (no per-unit licensing)

**Compatible Devices**:
- Windows PC (Windows 7/8/10/11 with USB port)
- Android smartphone (Android 5.0+ with USB OTG support)
- Android tablet (Android 5.0+ with USB OTG support)

**Ordering**: **TK4-PRG-NANO** (order separately from TK4 unit)

#### Software: Dedicated Application

**Availability**:
- **Windows version**: Download from Teklab website or supplied on USB drive
- **Android version**: Download from Google Play Store or Teklab website (search "Teklab TK4")
- **Free software**: No license fees, no subscription
- **Automatic updates**: New features added via App updates (no hardware changes required)
- **Multilingual**: Multiple language support

**App Features**:
- Real-time monitoring (valve status, sensor status, cycle times)
- Parameter configuration (modify timings, alarm settings, delays)
- Profile management (save/load configuration profiles for standardization)
- Data logging (view operation history, alarm events, valve cycles)
- Firmware update (update TK4 firmware via Nano Interface)
- Password protection (secure access to prevent unauthorized changes)
- Built-in help system (parameter explanations, troubleshooting guides)

### 9.2 Operating Modes

#### Powered Mode (TK4 Energized)

**Full Functionality**:
- ✅ Real-time monitoring: Live valve status, sensor readings, cycle timers
- ✅ Active configuration: Change parameters while unit operating
- ✅ Immediate testing: Verify parameter changes in real-time
- ✅ Data logging: Access operation history, alarm events, valve cycle count
- ✅ Diagnostics: Electronics temperature, supply voltage, communication errors

**Use Cases**:
- Field optimization (adjust timings based on observed system behavior)
- Troubleshooting (view alarm history, check sensor status)
- Performance monitoring (track valve cycles for predictive maintenance)

#### Not Powered Mode (TK4 NOT Energized)

**Basic Configuration**:
- ✅ Functioning timings (valve open/close delays, cycle times)
- ✅ Alarm delays (time before alarm triggers)
- ✅ Sensor sensitivity settings
- ✅ Password configuration
- ⚠️ No real-time monitoring (unit must be powered for live data)

**Use Cases**:
- **Pre-commissioning**: Configure units in workshop before installation
- **Factory settings verification**: Check configuration before shipment
- **In-house customization**: Pre-configure units for specific applications without external power
- **Inventory management**: Pre-set parameters for common applications, store ready-to-install

**Energy Source**: Nano Interface powered by USB dongle (no external TK4 power required for basic configuration)

### 9.3 Key Connectivity Advantages

#### Extremely Easy-to-Use

**No Enclosure Opening**:
- NFC works **through standard plastic enclosures** (5-10cm proximity)
- No screwdrivers, no panel removal, no cable connections
- Ideal for sealed installations or hazardous environments

**Intuitive Interface**:
- App guides user through parameter selection
- Clear parameter descriptions and valid ranges
- Immediate feedback on configuration changes
- Undo/redo functionality for safe experimentation

#### Highly Compact & Cost Effective

**No Additional Hardware on Unit**:
- TK4 maintains **same compact design as TK3+** (no external antenna, no display)
- NFC electronics integrated internally (no impact on installation footprint)

**Low-Cost Dongle**:
- One **TK4-PRG-NANO** dongle (~€100-150) configures unlimited TK4 units
- No expensive proprietary programming devices (€1000+) required
- Free App (no software licensing costs)

**ROI Example**: Configure 10 TK4 units → €10-15 per unit connectivity cost vs €1000+ for traditional programming systems

#### Highly Safe & Secure

**Password Protection**:
- **Master password**: Full access to all parameters (configurable via App)
- **User password**: Limited access (view-only or restricted parameters - optional)
- **Password recovery**: Contact Teklab support with unit serial number
- **Access log**: Tracks who configured unit and when (requires password to view)

**Limited Range Operation**:
- **5-10cm proximity required**: Prevents unauthorized access from distance
- **Point-to-point connection**: Only one device connected at a time
- **No network vulnerability**: No Wi-Fi, Bluetooth, or internet connectivity (isolated system)

**Physical Security**:
- Wireless works through plastic enclosures but **NOT through metal** (metal enclosures provide inherent security barrier)
- Installation in locked panels provides additional access control

#### Really Flexible

**Real-Time Parameter Adjustment**:
- Modify functioning parameters **while unit operates** (no downtime)
- Observe immediate impact of changes on system behavior
- Fine-tune settings iteratively for optimal performance

**Configuration Profiles**:
- **Save configuration** from optimized unit as profile in App
- **Load profile** to other units for standardization
- **Version control**: Maintain multiple profile versions (e.g., "Summer Settings", "Winter Settings")

**Multi-Unit Management**:
- Configure 10-20 units in typical site visit (1-2 minutes per unit)
- Standardize settings across compressor pack
- Document configurations for future reference

#### Open for the Future

**Continuous Feature Addition**:
- Teklab in contact with customers for feature requests
- **App updates** deliver new functionality without hardware changes
- **Firmware updates** via Nano Interface (over-the-air equivalent)

**Recent Feature Additions** (examples):
- Advanced diagnostics (valve cycle histogram, temperature trending)
- Configuration comparison tool (compare two units side-by-side)
- QR code export (configuration as QR code for documentation)

**Future Roadmap** (subject to development):
- Cloud backup of configuration profiles
- Automated reporting (maintenance schedules based on valve cycles)
- Integration with Teklab support portal (remote diagnostics assistance)

### 9.4 Configuration Parameters Accessible via Nano Interface

#### Basic Functioning Parameters

| Parameter | Range | Description | Powered/Unpowered |
|-----------|-------|-------------|-------------------|
| **Valve Opening Time** | 1-30 seconds | Duration valve remains open to inject oil | Both |
| **Valve Closing Time** | 1-60 seconds | Delay before valve closes after level reached | Both |
| **Cycle Interval** | 10-600 seconds | Time between oil injection cycles | Both |
| **Alarm Delay** | 5-300 seconds | Delay before alarm triggers on low level | Both |

#### Advanced Parameters

| Parameter | Range | Description | Powered/Unpowered |
|-----------|-------|-------------|-------------------|
| **Sensor Sensitivity** | Low/Medium/High | Adjust for foam, turbulence, liquid properties | Both |
| **LED Brightness** | 0-100% | Adjust status LED visibility | Both |
| **Alarm Hysteresis** | 1-60 seconds | Prevent alarm chatter on borderline conditions | Both |
| **Manual Test Mode** | Enable/Disable | Force valve operation for testing | Powered only |

#### Security & Diagnostics

| Parameter | Access Level | Description | Powered/Unpowered |
|-----------|--------------|-------------|-------------------|
| **Master Password** | Master only | Set/change master password | Both |
| **User Password** | Master only | Set/change user password (optional) | Both |
| **Factory Reset** | Master only | Restore all parameters to factory defaults | Both |
| **Access Log** | Master/User | View configuration change history | Powered only |
| **Valve Cycle Count** | Read-only | Total valve operations (maintenance indicator) | Powered only |
| **Alarm Event Count** | Read-only | Total alarm activations | Powered only |

### 9.5 Typical Usage Workflows

#### Workflow 1: Initial Commissioning (New Installation)

**Step 1: Pre-Configuration (Workshop - Unpowered)**
1. Remove TK4 from packaging (leave unpowered)
2. Connect TK4-PRG-NANO dongle to laptop
3. Launch Teklab App, approach TK4 with dongle (5-10cm)
4. App detects TK4 automatically
5. Configure basic parameters:
   - Valve opening time: 5 seconds (example)
   - Alarm delay: 30 seconds (example)
   - Set master password: "TeklabAdmin2025" (example)
6. Save configuration, label unit with settings
7. Repeat for all units in batch (standardized configuration)

**Step 2: Installation (Site)**
1. Mount TK4 on compressor, connect piping
2. Wire power supply (24V AC/DC)
3. Power on → TK4 operates with pre-configured settings (no on-site configuration needed)

**Step 3: Field Verification (Site - Powered)**
1. Approach TK4 with Android tablet + dongle
2. Connect via App (enter password)
3. View real-time valve status, verify proper operation
4. Fine-tune timing if needed (observe 2-3 cycles)
5. Save optimized settings, document configuration

**Time Saved**: 15-20 minutes per unit (vs opening enclosure, setting DIP switches, testing, closing)

#### Workflow 2: Field Optimization (Existing Installation)

**Scenario**: Compressor oil level cycling too frequently (valve opens/closes every 2 minutes instead of optimal 5 minutes)

**Steps**:
1. Approach operating TK4 with smartphone + dongle
2. Connect via App (enter password)
3. View real-time monitoring:
   - Current cycle interval: 120 seconds (2 minutes)
   - Valve opening time: 10 seconds
   - Observation: Valve injecting too much oil per cycle
4. Adjust parameter:
   - Reduce valve opening time: 10 → 6 seconds
5. Observe next 3 cycles (monitor via App):
   - Cycle interval increases to 280 seconds (4.7 minutes) ✓
6. Save optimized settings
7. Document change in maintenance log

**Result**: Oil consumption reduced, compressor crankcase oil level stabilized, no unnecessary valve cycling

#### Workflow 3: Troubleshooting (Alarm Condition)

**Scenario**: TK4 alarm triggered, compressor crankcase oil level low

**Steps**:
1. Approach TK4 with tablet + dongle (unit remains powered and alarming)
2. Connect via App (enter password)
3. View diagnostics:
   - Alarm status: Active (low level alarm)
   - Alarm event count: 5 (recent increase)
   - Valve cycle count: 1,247 cycles
   - Last valve operation: 15 minutes ago (should be ~5 minutes)
   - Sensor status: Air detected (no oil reaching sensor)
4. Root cause identified: **Oil supply issue** (valve operating but oil not reaching crankcase)
   - Check oil separator level (empty)
   - Check oil supply line (restriction or valve closed)
5. Fix root cause (refill separator, open isolation valve)
6. Reset alarm via App
7. Monitor next 2-3 cycles to verify normal operation restored

**Time Saved**: Immediate diagnostics (no guessing, no trial-and-error), targeted troubleshooting

#### Workflow 4: Multi-Unit Standardization (Compressor Pack)

**Scenario**: 8-compressor pack, need to standardize oil level regulation settings

**Steps**:
1. Optimize first compressor TK4 settings (see Workflow 2)
2. Save configuration as profile in App:
   - Profile name: "CompressorPack_SummerSettings_2025"
3. Visit other 7 TK4 units sequentially:
   - Approach each unit with tablet + dongle
   - Connect via App
   - Load saved profile → Automatically configures unit with same settings
   - Verify and save (30 seconds per unit)
4. Document configuration across all units (export profile as PDF report)

**Time Saved**: 10-15 minutes per unit (vs manual configuration + verification)

**Consistency**: All units configured identically (eliminates human error, variation)

### 9.6 Security Best Practices

#### Password Management

**Recommendations**:
- ✅ **Always set master password** during commissioning (prevents unauthorized changes)
- ✅ Use **strong passwords** (8+ characters, mix of letters/numbers/symbols)
- ✅ **Document passwords securely** (password manager, sealed envelope in site documentation)
- ✅ Change password if staff turnover (terminated employees lose access)
- ⚠️ **Do NOT use default password** (if factory default exists, change immediately)

**Password Recovery**:
- If password forgotten: Contact Teklab support with unit serial number
- Factory reset option: May require physical access to DIP switch (check manual) - **WARNING: Erases all configuration**

#### Physical Access Control

**Installation Recommendations**:
- Install TK4 in **locked electrical panels** when possible (prevents unauthorized proximity access)
- For open installations: **Password protection is critical** (only security layer)
- High-security environments: Consider **metal enclosure** (blocks NFC, requires panel opening for access)

#### Access Logging

**Enable Access Log** (via App):
- Records all configuration changes with timestamp
- Tracks password-authenticated users (if multiple user accounts configured)
- Review log periodically for unauthorized access attempts
- Export log for compliance documentation

### 9.7 Technical Specifications

#### NFC Communication

| Parameter | Specification |
|-----------|--------------|
| **Protocol** | NFC (Near-Field Communication), ISO 14443 |
| **Operating Frequency** | 13.56 MHz |
| **Operating Range** | 5-10cm typical (through plastic), 2-5cm (through thick plastic) |
| **Data Rate** | 106 kbps |
| **Enclosure Penetration** | Plastic ✓, Metal ✗ |

#### TK4-PRG-NANO Dongle

| Parameter | Specification |
|-----------|--------------|
| **USB Interface** | USB 2.0 or higher (backward compatible) |
| **Power Consumption** | USB bus powered (no external power required) |
| **Operating Temperature** | 0°C to +50°C |
| **Storage Temperature** | -20°C to +70°C |
| **Dimensions** | Approximately 60mm × 20mm × 10mm (compact) |
| **Weight** | Approximately 15g |
| **Cable Length** | 1m USB cable included (extension cables supported) |

#### Software Compatibility

| Platform | Requirements |
|----------|--------------|
| **Windows** | Windows 7/8/10/11, USB port, 50MB disk space |
| **Android** | Android 5.0 or higher, USB OTG support, 20MB storage |
| **iOS** | Not currently supported (USB OTG limitation) |

#### Security

| Feature | Specification |
|---------|--------------|
| **Password Protection** | AES-128 encryption, 8-16 character passwords |
| **Access Control** | Master/User password levels |
| **Communication Range** | Limited to 5-10cm (prevents remote unauthorized access) |
| **Connection Type** | Point-to-point (one device at a time) |
| **Network Isolation** | No Wi-Fi, Bluetooth, or internet connectivity |

### 9.8 Ordering Information

#### Nano Interface Dongle

**Ordering Code**: **TK4-PRG-NANO**

**Package Includes**:
- USB dongle with NFC transceiver
- 1m USB cable (if needed for specific devices)
- Quick start guide (printed)
- Access to downloadable App (Windows and Android)

**Not Included** (user supplied):
- Windows PC or Android device
- TK4 unit (order separately - see Section 3)

**Pricing**: Contact Teklab for current pricing (~€100-150 typical)

**Quantity Recommendation**:
- **Small installations** (1-5 TK4 units): 1 dongle sufficient
- **Medium installations** (6-20 TK4 units): 1 dongle per service technician
- **Large installations** (20+ TK4 units, multi-site): 2-3 dongles (commissioning team, maintenance team, spare)

#### Accessories (Optional)

**USB OTG Cable for Android**:
- If Android device lacks USB port (USB-C or Micro-USB to USB-A adapter required)
- **Not included** with TK4-PRG-NANO (user supplied)

**Protective Case**:
- Hard case for dongle protection during field work (optional)
- Contact Teklab for availability

### 9.9 Integration with TK4 Operation

#### Nano Interface Does NOT Interfere with Operation

**Critical Design Principle**: Nano Interface is **read/write interface only**, not required for TK4 operation.

**TK4 Operates Independently**:
- ✅ Oil level regulation continues even if Nano Interface never used
- ✅ No dongle required during normal operation (configure once, remove dongle)
- ✅ Configuration stored in TK4 non-volatile memory (survives power loss)

**Use Cases**:
- **Commissioning**: Configure via Nano Interface, remove dongle, TK4 operates autonomously
- **Maintenance**: Connect dongle for diagnostics/optimization, disconnect after completion
- **Emergency**: If dongle lost/broken, TK4 continues operation with last saved configuration

#### Relationship with Modbus RS485 (TK4 Only)

**TK4 Standard Model**: **NFC Nano Interface only** (no Modbus RS485)

**Nano Interface Use Cases for TK4**:
1. **Initial commissioning**: Configure all parameters via NFC
2. **Field optimization**: Adjust timings based on observed system behavior
3. **Troubleshooting**: View diagnostics, alarm history, valve cycle count
4. **Periodic maintenance**: Download operation logs, verify settings

**No Remote Monitoring**: TK4 (without Modbus) cannot be monitored from control room - requires site visit with Nano Interface for status checks.

**Upgrade Path**: For remote monitoring capability, consider **TK4-MB** (see next section or TK4_MB_SERIES_COMPLETE.md)

---

**Language**: English  
**Product Family**: TK4 Smart Oil Level Regulators (46/80/130 bar) with Modbus RS485 + NFC  
**Category**: Oil_Level_Regulators  
**Keywords**: TK4, smart oil level regulator, Modbus RS485, NFC configuration, BMS integration, remote monitoring, 46 bar, 80 bar, 130 bar, CO2 subcritical, CO2 transcritical, field programmable, predictive maintenance

**© 2025 Teklab. All rights reserved.**
