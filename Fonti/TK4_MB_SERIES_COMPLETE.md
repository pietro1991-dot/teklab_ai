---
category: Oil_Level_Regulators
keywords:
- TK4-MB
- TK4 MB Series
- TK4-MB 46 bar
- TK4-MB 80 bar
- TK4-MB 130 bar
- Modbus RTU
- RS485 serial
- NFC configuration
- TK4-PRG-NANO
- dual communication
- remote monitoring
- BMS SCADA integration
- factory configured
- plug and play serial
- CO2 transcritical
- system controller
language: EN
product: TK4_MB_Series
document_type: unified_complete
last_updated: 2025-11-15
---

# TK4 MB Series - Complete Product Documentation

**Smart Oil Level Regulators with Integrated Modbus RTU Serial Connectivity**

---

## 📋 Document Structure

This unified document covers the complete TK4 MB product family organized in the following sections:

1. **Product Family Overview** - Series description and variant comparison
2. **Variant-Specific Details** - Technical specs for each pressure variant (46/80/130 bar)
3. **Common Features** - Shared technology across all variants
4. **Connectivity Features** - Modbus RTU serial communication
5. **Technical Specifications** - Electrical, mechanical, environmental specs
6. **Applications & Selection** - Use cases and variant selection guide
7. **Installation & Service** - Mounting, wiring, configuration, maintenance
8. **FAQ** - Frequently asked questions
9. **Connectivity Features (Modbus RTU + NFC)** - Dual communication: wired RS485 + wireless NFC configuration

---

## 1. PRODUCT FAMILY OVERVIEW

### TK4 MB Series Description

The **TK4 MB Series** is a family of smart oil level regulators combining electro-optic level detection, integrated solenoid valve, and Modbus RTU serial connectivity via RS485. Available in three pressure variants to cover standard refrigeration through CO2 transcritical applications with system controller integration capability.

**Core Technology:**
- Electro-optic IR sensor (fused glass hermetic seal)
- Integrated NC solenoid valve (20VA for 46 bar, 30VA for 80/130 bar)
- **Modbus RTU serial communication** via RS485 for system controller integration
- Factory-configured (no field programming required - plug and play)
- Automatic operation with centralized serial monitoring
- Dual LEFT/RIGHT mounting capability
- Two-part serviceable design

**Product Family:**

| Model | Max Pressure | MOPD | Valve Power | Primary Applications | Connectivity |
|-------|-------------|------|-------------|---------------------|--------------|
| **TK4 MB 46 bar** | 46 bar | 26 bar | 20VA | Standard refrigeration + serial controller (R134a, R404A, R407C, R410A) | Modbus RTU |
| **TK4 MB 80 bar** | 80 bar | 60 bar | 30VA | CO2 subcritical + serial controller, R410A hot climate | Modbus RTU |
| **TK4 MB 130 bar** | 130 bar | 100 bar | 30VA | CO2 transcritical + serial controller, extreme high-pressure systems | Modbus RTU |

**Key Differentiator vs TK4 Series:**
- **TK4 (standard)**: Modbus RS485 + NFC wireless configuration (smartphone/tablet)
- **TK4 MB**: Modbus RTU serial only (RS485), factory-configured, no NFC wireless config

**TK4 MB is simpler:**
- Factory pre-configured (no field programming needed)
- Plug-and-play serial connectivity
- Lower cost than TK4 standard (no NFC hardware)
- Ideal for fixed installations with system controllers

**Selection Criteria:**
- Calculate **MOPD** (Separator Pressure - Crankcase Pressure)
- Determine if serial controller integration required (TK4 MB) or BMS/SCADA with field config (TK4 standard)
- Choose pressure variant with 20-30% safety margin above calculated MOPD
- Consider cost: TK4 MB is ~30% less expensive than TK4 standard (no NFC), but 50-60% more than TK3+

**Common Characteristics (All TK4 MB Variants):**
- Modbus RTU for real-time serial monitoring and data logging
- Factory-configured (no field programming required)
- Plug-and-play serial connectivity (RS485 daisy-chain)
- Remote diagnostics via Modbus network
- Same physical mounting as TK3+/TK4 (drop-in replacement)
- Sight-glass replacement (3/4/6-hole flanges via adapters)
- IP65 enclosure protection
- CE certified (EMC + LVD)
- Service without depressurization

---

## 2. VARIANT-SPECIFIC DETAILS

### 2.1 TK4 MB 46 bar - Standard Pressure Serial Variant

**Overview:**
Standard pressure smart oil level regulator with Modbus RTU serial connectivity for conventional refrigeration systems requiring system controller integration. Most versatile variant suitable for R134a, R404A, R407C, R410A with centralized serial monitoring.

**Pressure Ratings:**
- Max Working Pressure: **46 bar**
- MOPD: **26 bar**
- Typical separator pressure range: 10-35 bar
- Typical crankcase pressure range: 2-10 bar

**Power Specifications:**
- Power consumption: **20VA** (sensor + valve + serial communication)
- Supply voltage: 24VAC ±10% or 230VAC ±10%

**Primary Applications:**
- Commercial refrigeration with system controller (supermarket racks, cold storage)
- Multi-compressor systems requiring centralized serial data collection
- Industrial facilities with RS485-based monitoring systems
- System controller integration (no BMS/SCADA, direct serial control)
- R410A air conditioning with serial monitoring (normal climate)
- Fixed installations where field programming not required

**Connectivity Features:**
- **Modbus RTU Serial**: Real-time oil level status, valve state, alarm conditions, operating hours via RS485
- **Factory-Configured**: Pre-programmed Modbus address, baud rate (typically 9600 bps), no field config needed
- **Plug-and-Play**: Connect RS485, power on, start monitoring
- **Data Logging**: Historical data via system controller

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

**When to Choose TK4 MB 46 bar:**
- System controller integration via Modbus RTU/RS485 required
- Centralized serial monitoring of multiple compressors needed
- Factory-configured operation preferred (no field programming)
- Separator pressure < 35 bar, differential < 26 bar
- Lower cost than TK4 standard (no NFC hardware)

**Cost Consideration:**
- ~30% less expensive than TK4 standard (no NFC)
- ~50-60% more expensive than TK3+ 46 bar
- Justified when system controller integration eliminates site visits

---

### 2.2 TK4 MB 80 bar - High Pressure Serial Variant

**Overview:**
High-pressure smart oil level regulator with Modbus RTU serial connectivity designed for CO2 subcritical systems and high-temperature R410A applications requiring system controller integration. Reinforced components with 30VA valve for 80 bar maximum working pressure.

**Pressure Ratings:**
- Max Working Pressure: **80 bar**
- MOPD: **60 bar**
- Typical separator pressure range: 30-70 bar
- Typical crankcase pressure range: 5-20 bar

**Power Specifications:**
- Power consumption: **30VA** (sensor + reinforced valve + serial communication)
- Supply voltage: 24VAC ±10% or 230VAC ±10%
- **Note**: Higher power consumption than 46 bar variant (30VA vs 20VA)

**Primary Applications:**
- CO2 subcritical refrigeration with system controller (40-70 bar separator pressure)
- R410A hot climate with serial monitoring (50-55°C condensing)
- High-pressure oil return systems requiring centralized serial monitoring
- Supermarket CO2 cascade systems with system controller integration
- Industrial CO2 facilities with RS485-based control

**Connectivity Features:**
- **Modbus RTU Serial**: Critical for CO2 systems requiring pressure/level serial monitoring
- **Factory-Configured**: Pre-programmed for CO2 subcritical parameters
- **Remote Diagnostics**: Troubleshoot high-pressure systems via serial controller

**Dimensions:**
- Height: 107.75 mm
- Width (electronics): 59.5 mm
- Total width (with projections): 78 mm

**Weight:** 850-1050g (heavier valve body vs 46 bar)

**Refrigerant Compatibility:**
- CO2 subcritical (primary application)
- R410A hot climate (50°C+ condensing)
- All refrigerants compatible with 46 bar variant

**When to Choose TK4 MB 80 bar:**
- CO2 subcritical systems requiring system controller integration (differential 30-60 bar)
- R410A hot climate with serial monitoring (differential > 26 bar)
- High-pressure separator (50-70 bar) with centralized serial data collection
- Factory-configured CO2 subcritical operation (no field programming needed)

**Key Difference vs TK4 MB 46 bar:**
- Reinforced valve body and seat materials
- 30VA power consumption (vs 20VA for 46 bar)
- 80 bar rated glass dome (thicker wall)
- Higher MOPD capability (60 vs 26 bar)
- Same Modbus RTU connectivity
- ~15% higher cost than TK4 MB 46 bar

---

### 2.3 TK4 MB 130 bar - Very High Pressure Serial Variant

**Overview:**
Maximum pressure smart oil level regulator with Modbus RTU serial connectivity specifically engineered for CO2 transcritical refrigeration. Heavy-duty construction with 30VA valve handles extreme pressures (gas cooler 80-120 bar) with full system controller integration.

**Pressure Ratings:**
- Max Working Pressure: **130 bar**
- MOPD: **100 bar**
- Typical separator pressure range: 80-120 bar (gas cooler outlet)
- Typical crankcase pressure range: 30-40 bar

**Power Specifications:**
- Power consumption: **30VA** (sensor + heavy-duty valve + serial communication)
- Supply voltage: 24VAC ±10% or 230VAC ±10%
- **Note**: Same power as 80 bar variant (30VA)

**Primary Applications:**
- CO2 transcritical refrigeration systems with system controller
- CO2 heat pump applications with serial monitoring (transcritical cycle)
- Supermarket transcritical booster systems with system controller integration
- Extreme high-pressure systems requiring centralized serial monitoring
- CO2 transcritical facilities with RS485-based control

**Connectivity Features:**
- **Modbus RTU Serial**: Essential for transcritical systems (critical pressure serial monitoring)
- **Factory-Configured**: Pre-programmed for transcritical gas cooler conditions
- **Remote Diagnostics**: Critical for high-pressure safety serial monitoring

**Dimensions:**
- Height: 107.75 mm
- Width (electronics): 59.5 mm
- Total width (with projections): 78 mm

**Weight:** 900-1100g (heaviest valve construction)

**Refrigerant Compatibility:**
- CO2 transcritical (primary and exclusive application)
- Not typically used for HFC/HFO refrigerants (overkill)

**When to Choose TK4 MB 130 bar:**
- CO2 transcritical ONLY with system controller integration
- Gas cooler pressure > 80 bar with serial monitoring required
- Differential pressure 60-100 bar with centralized serial data logging
- Safety-critical applications requiring real-time pressure serial alerts
- Factory-configured transcritical operation (no field programming needed)

**Key Difference vs TK4 MB 80 bar:**
- Maximum reinforced valve body (heavy-duty)
- 130 bar rated glass dome (maximum thickness)
- MOPD 100 bar (highest in TK4 MB series)
- Same Modbus RTU connectivity
- Same 30VA power consumption
- ~25% higher cost vs TK4 MB 80 bar

**Design Notes:**
- Over-specification for HFC systems (use TK4 MB 46 or 80 bar instead)
- Same external dimensions as TK4 MB 80 bar (interchangeable mounting)
- Same electronic module across all TK4 MB variants (pressure rating in valve/sensor only)
- Modbus RTU features identical across all variants

---

## 3. COMMON FEATURES (All TK4 MB Variants)

### 3.1 Integration & Automation

**Complete Integrated System:**
- Electro-optic sensor + solenoid valve + control + Modbus RTU serial in single unit
- No external controller, wiring harnesses, or I/O modules required
- Factory-configured and tested, plug-and-play RS485 connection
- Automatic operation with serial connectivity available on demand

**Automatic Operation:**
- Self-contained sensor + valve + control (operates identically to TK3+ for basic function)
- No PLC programming required for automatic oil level control
- Modbus RTU serial is optional enhancement (not required for basic operation)
- Future-proof: serial monitoring without hardware replacement

**Dual LEFT/RIGHT Mounting:**
- Same product works on either side of compressor
- Electronic module and valve body rotate to match installation side
- **50% inventory SKU reduction** (no separate left/right models)
- Installation flexibility (choose mounting side during installation)

### 3.2 Revolutionary Design Features

**Sight-Glass Replacement:**
- Direct mounting to 3/4/6-hole compressor flanges (via Teklab adapters)
- Maintains visual inspection capability (LED indication replaces glass viewing)
- Combines visual + automatic electronic control + serial connectivity
- Eliminates separate sight-glass + sensor + serial connectivity installations

**Two-Part Modular Design:**
- **Part 1** (permanent): Sensor adapter + valve body
  - Remains on compressor during service
  - Brazed/flanged connections intact
- **Part 2** (replaceable): Electronic module + Modbus RTU board
  - 5-10 minute replacement time
  - No system depressurization required
  - No refrigerant recovery
  - Factory-configured module (no field programming)

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
- Self-diagnostic LED indication + Modbus RTU status reporting

### 3.4 Electrical Features

**Power Supply:**
- **24VAC ±10%** or **230VAC ±10%** (model dependent - specify at order)
- Power consumption: 
  - **20VA** for TK4 MB 46 bar (sensor + valve + serial)
  - **30VA** for TK4 MB 80/130 bar (sensor + reinforced valve + serial)
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

| Compressors | TK4 MB 46 bar | TK4 MB 80/130 bar | Recommended Transformer |
|-------------|---------------|-------------------|-------------------------|
| 1 unit | 20VA | 30VA | 40VA minimum |
| 2 units | 40VA | 60VA | 80VA minimum |
| 3 units | 60VA | 90VA | 120VA minimum |
| 4 units | 80VA | 120VA | 150VA minimum |
| 6 units | 120VA | 180VA | 230VA minimum |

*Note: Size transformer 50-60% above total load for inrush current and margin.*

### 3.5 Installation & Reliability

**Reduced Leak Points:**
- TK4 MB system: **2 junctions** (flange + oil inlet)
- Separate components: **6+ junctions** (sensor flange, valve inlet/outlet, piping)
- Fewer leak points = higher system reliability

**Simplified Wiring:**
- TK4 MB: **6 wires total** (2 power + 2 relay + 2 Modbus RTU RS485)
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
- Electronic module (including Modbus RTU board) replaceable without system depressurizing
- Module secured with screws (no special tools)
- Disconnect power → remove screws → lift module → replace
- 5-10 minute service time vs hours for valve replacement

---

## 4. CONNECTIVITY FEATURES

### 4.1 Modbus RTU Serial Communication

**Protocol & Specifications:**
- **Protocol**: Modbus RTU (industry standard serial protocol)
- **Physical**: RS485 twisted pair (2-wire, daisy-chain topology)
- **Baud Rate**: 9600 bps (factory default), 19200/38400 bps available via custom order
- **Data Format**: 8N1 (8 data bits, no parity, 1 stop bit) - factory default
- **Address Range**: 1-247 (factory-configured per unit)
- **Max Distance**: 1200m (twisted pair cable)
- **Termination**: 120Ω resistors at both ends of network

**Real-Time Serial Monitoring Data:**
- Oil level status (OK / LOW / ALARM)
- Valve state (OPEN / CLOSED)
- Alarm status and history
- Operating hours (valve and sensor)
- Valve cycle counter (predictive maintenance)
- Module temperature
- Configuration parameters (read-only)

**System Controller Integration Benefits:**
- Centralized serial monitoring of multiple compressors
- Historical data logging for trend analysis
- Predictive maintenance (valve cycle tracking)
- Remote diagnostics (troubleshoot via serial controller)
- Alarm forwarding to system controller
- Energy optimization (oil return pattern analysis)

**Typical Polling Rate:**
- 1-5 seconds per TK4 MB unit (depends on system controller configuration)
- Faster polling for critical applications (CO2 transcritical)
- Slower polling for energy conservation

### 4.2 Factory Configuration

**Pre-Configured Parameters:**
- **Modbus Address**: Unique address (1-247) assigned at factory or specified at order
- **Baud Rate**: 9600 bps default (or custom-ordered rate)
- **Data Format**: 8N1 default (or custom-ordered format)
- **Oil Level Setpoints**: Factory-optimized for compressor crankcase operation
- **Alarm Delays**: Pre-configured delay (60-120 sec) to prevent nuisance alarms

**Configuration Process:**
1. Order TK4 MB with desired Modbus address (specify at order)
2. Factory programs and tests unit
3. Unit ships ready to connect (plug-and-play)
4. Connect RS485, power on, start monitoring

**Advantages:**
- **No field programming** required (eliminates commissioning errors)
- **Faster installation** (no configuration tools needed)
- **Lower cost** than TK4 standard (no NFC hardware)
- **Simplified inventory** (fewer spare parts vs configurable models)

**Limitations:**
- **Fixed configuration** (address/baud rate change requires factory service or replacement)
- **No on-site parameter adjustment** (setpoints pre-configured at factory)
- **Not suitable for flexible installations** (use TK4 standard with NFC if parameters change frequently)

### 4.3 TK4 MB vs TK4 Standard Comparison

**TK4 MB (Modbus RTU Only):**
- Factory-configured (Modbus address, baud rate pre-programmed)
- Plug-and-play serial connectivity
- No NFC wireless configuration capability
- Lower cost (~30% less than TK4 standard)
- Ideal for fixed installations with system controllers

**TK4 Standard (Modbus RS485 + NFC):**
- Field-configurable via NFC smartphone/tablet
- Modbus RS485 for BMS/SCADA integration
- Full parameter access (setpoints, timings, Modbus settings)
- Higher cost (NFC hardware included)
- Ideal for BMS integration with field flexibility

**When TK4 MB is Better:**
- System controller integration via RS485 (no BMS/SCADA)
- Fixed installation where parameters rarely change
- Factory-configured operation preferred
- Cost-sensitive applications requiring serial connectivity

**When TK4 Standard is Better:**
- BMS/SCADA integration required
- Field programmability essential (parameter changes on-site)
- Smartphone/tablet configuration tools preferred
- Future flexibility needed (address/baud rate changes)

---

## 5. TECHNICAL SPECIFICATIONS

### 5.1 Electrical Specifications (Variant-Specific)

| Parameter | TK4 MB 46 bar | TK4 MB 80/130 bar |
|-----------|--------------|-------------------|
| Supply Voltage | 24VAC ±10% or 230VAC ±10% | 24VAC ±10% or 230VAC ±10% |
| Supply Current | **20VA** per unit | **30VA** per unit |
| Electrical Connection | 9.4mm EN175301-803 OR M12/M16 glands | Same |
| Output Signal | Contact-free relay (NO + NC) | Same |
| Relay Rating | 230VAC @ 2A resistive | Same |
| Cable Type | PVC CEI 20-22 rated -20°C to +70°C | Same |
| Cable Lengths | 1m (glands), 3m or 6m (connectors) | Same |
| Frequency | 50/60 Hz | 50/60 Hz |

### 5.2 Modbus RTU Serial Specifications

| Parameter | Specification |
|-----------|--------------|
| Protocol | Modbus RTU (industry standard) |
| Physical Layer | RS485 twisted pair (2-wire) |
| Baud Rate | 9600 bps (default), 19200/38400 bps (custom order) |
| Data Format | 8N1 (8 data, no parity, 1 stop) default |
| Address Range | 1-247 (factory-configured) |
| Max Distance | 1200m (twisted pair) |
| Termination | 120Ω at endpoints |
| Configuration | Factory-configured (no field programming) |
| Monitoring | Read-only (system controller polling) |

### 5.3 Mechanical Specifications (Variant-Specific)

| Parameter | TK4 MB 46 bar | TK4 MB 80 bar | TK4 MB 130 bar |
|-----------|--------------|--------------|---------------|
| Housing Material | Nickel-plated steel + fused glass | Same | Same |
| Electronics Housing | PA glass fiber + Modbus RTU board | Same | Same |
| Enclosure Protection | IP65 | IP65 | IP65 |
| Flange Connection | 3/4/6-hole (via adapters) | Same | Same |
| Oil Return Line | 7/16-20 UNF male | Same | Same |
| Height (mm) | 108.25 | 107.75 | 107.75 |
| Width Electronics (mm) | 59.5 | 59.5 | 59.5 |
| Total Width (mm) | 78 | 78 | 78 |
| Weight (g) | 800-1000 | 850-1050 | 900-1100 |
| Module Weight (g) | 150-200 (replaceable) | 150-200 | 150-200 |

### 5.4 Environmental & Pressure Specifications

| Parameter | TK4 MB 46 bar | TK4 MB 80 bar | TK4 MB 130 bar |
|-----------|--------------|--------------|---------------|
| Media Temperature | -40°C to +85°C | -40°C to +85°C | -40°C to +85°C |
| Ambient Temperature | -40°C to +60°C | -40°C to +60°C | -40°C to +60°C |
| Max Working Pressure | **46 bar** | **80 bar** | **130 bar** |
| MOPD (Max Differential) | **26 bar** | **60 bar** | **100 bar** |
| Humidity | 5-95% RH non-condensing | Same | Same |
| Vibration | IEC 60068-2-6 compliant | Same | Same |

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

| Parameter | TK4 MB 46 bar | TK4 MB 80 bar | TK4 MB 130 bar |
|-----------|--------------|--------------|---------------|
| Valve Type | NC solenoid | NC solenoid | NC solenoid |
| Power Consumption | 20VA | 30VA | 30VA |
| Operation | Automatic (sensor-controlled) | Same | Same |
| Pressure Rating | 46 bar, MOPD 26 bar | 80 bar, MOPD 60 bar | 130 bar, MOPD 100 bar |
| Serviceable Coil | Yes (no depressurization) | Yes | Yes |
| Valve Body Material | Nickel-plated steel | Reinforced steel | Heavy-duty steel |
| Response Time | < 2 seconds | < 2 seconds | < 2 seconds |

### 5.7 Compliance (All Variants)

| Standard | Description |
|----------|-------------|
| 2014/30/UE | EMC Directive (Electromagnetic Compatibility) |
| 2014/35/UE | Low Voltage Directive |
| CE Marking | Compliant and certified |
| IP Rating | IP65 (dust-tight, water jet protected) |
| Modbus | Modbus RTU compliant (RS485) |

### 5.8 Refrigerant & Oil Compatibility

**Refrigerants:**

| Variant | Compatible Refrigerants |
|---------|------------------------|
| TK4 MB 46 bar | R134a, R404A, R407C, R410A, R290, R600a, CO2 subcritical (if MOPD < 26 bar), Ammonia (approval required) |
| TK4 MB 80 bar | CO2 subcritical, R410A hot climate, all 46 bar refrigerants |
| TK4 MB 130 bar | CO2 transcritical (primary), all other refrigerants (overkill for HFC) |

**Oils:**
All variants compatible with: Mineral, POE, PAG, AB, PVE, and all synthetic oils (fused glass + nickel-plated steel = universal compatibility)

---

## 6. APPLICATIONS & SELECTION GUIDE

### 6.1 Application Examples by Variant

#### TK4 MB 46 bar Applications

**Commercial Refrigeration with System Controller:**
- Supermarket rack systems with RS485-based system controller
- Multi-store chain facilities (serial monitoring via system controller)
- Cold storage warehouses with centralized serial controller
- Facilities requiring RS485 connectivity (no BMS/SCADA)

**Industrial Refrigeration with Serial Controller:**
- Food processing plants (centralized serial data logging)
- Pharmaceutical storage (compliance documentation via serial controller)
- Brewery and beverage cooling (predictive maintenance via serial)

**System Controller Integration:**
- Chiller plants with system controller (R134a, R407C)
- Rooftop units with serial monitoring (R410A)
- Process cooling with centralized serial control

**Multi-Compressor Systems:**
- Parallel rack systems (3-6 compressors with serial controller monitoring)
- Automatic oil equalization with serial data logging
- Predictive maintenance via valve cycle tracking via serial

#### TK4 MB 80 bar Applications

**CO2 Subcritical Systems with System Controller:**
- Supermarket CO2 cascade systems (MT stage serial monitoring)
- Industrial CO2 refrigeration with system controller (40-70 bar)
- CO2 booster systems with serial remote diagnostics

**High-Pressure HFC Systems with Serial Monitoring:**
- R410A hot climate with serial alerts (50-55°C condensing)
- High-pressure oil separators requiring serial monitoring (50-70 bar)
- Industrial systems with system controller integration

**Extreme Differential Applications:**
- High separator pressure + low suction with serial monitoring
- Systems with 30-60 bar differential requiring serial data logging
- Safety-critical applications with real-time serial pressure alerts

#### TK4 MB 130 bar Applications

**CO2 Transcritical Systems with System Controller:**
- Supermarket transcritical CO2 systems with serial system controller
- Gas cooler outlet 80-120 bar with serial remote monitoring
- CO2 heat pumps with predictive maintenance via serial (transcritical cycle)

**Extreme High-Pressure with Serial Monitoring:**
- Industrial CO2 transcritical with centralized serial control
- Applications above 80 bar requiring real-time serial monitoring
- Differential pressure 60-100 bar with serial controller integration

### 6.2 Variant Selection Process

**Step 1: Determine Connectivity Requirement**
- **System controller integration via RS485 required?** → TK4 MB series (Modbus RTU)
- **BMS/SCADA integration with field config?** → TK4 standard series (Modbus RS485 + NFC)
- **Basic automatic control sufficient?** → TK3+ series (50-60% less expensive)

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
| 0-20 bar | 24-26 bar | **TK4 MB 46 bar** |
| 20-50 bar | 24-60 bar | **TK4 MB 80 bar** |
| 50-80 bar | 60-100 bar | **TK4 MB 130 bar** |
| > 80 bar | > 96 bar | **TK4 MB 130 bar** (maximum) |

**Step 5: Verify Application Match**
- CO2 transcritical → TK4 MB 130 bar (mandatory)
- CO2 subcritical → TK4 MB 80 bar or 130 bar (depending on MOPD)
- R410A hot climate → TK4 MB 80 bar (safety margin)
- Standard HFC with serial controller → TK4 MB 46 bar

### 6.3 Selection Examples

**Example 1: R404A Supermarket Rack with System Controller**
- Separator pressure: 28 bar
- Crankcase pressure: 4 bar
- MOPD: 28 - 4 = 24 bar
- Safety margin: 24 × 1.2 = 28.8 bar
- System controller: Required (Modbus RTU RS485)
- **Selection: TK4 MB 46 bar** → Acceptable, consider TK4 MB 80 bar for better margin

**Example 2: CO2 Subcritical System with System Controller**
- Separator pressure: 60 bar
- Crankcase pressure: 15 bar
- MOPD: 60 - 15 = 45 bar
- Safety margin: 45 × 1.2 = 54 bar
- System controller: Required (serial monitoring)
- **Selection: TK4 MB 80 bar (MOPD 60 bar)** → Perfect match

**Example 3: CO2 Transcritical System with System Controller**
- Gas cooler outlet: 100 bar
- Crankcase pressure: 35 bar
- MOPD: 100 - 35 = 65 bar
- Safety margin: 65 × 1.2 = 78 bar
- System controller: Required (critical serial monitoring)
- **Selection: TK4 MB 130 bar (MOPD 100 bar)** → Only option, ideal

**Example 4: R410A Standard Climate with System Controller**
- Separator pressure: 25 bar (40°C condensing)
- Crankcase pressure: 8 bar
- MOPD: 25 - 8 = 17 bar
- System controller: Desired (facility management)
- **Selection: TK4 MB 46 bar** → Ideal smart choice

**Example 5: R134a Chiller Plant with BMS (Not System Controller)**
- Separator pressure: 20 bar
- Crankcase pressure: 5 bar
- MOPD: 20 - 5 = 15 bar
- BMS/SCADA integration: Required (not just system controller)
- Field configuration: Needed (parameter adjustments)
- **Selection: TK4 standard 46 bar (not TK4 MB)** → NFC field config essential

### 6.4 TK4 MB vs TK4 vs TK3+ Decision Matrix

| Requirement | TK3+ Series | TK4 MB Series | TK4 Standard Series |
|------------|-------------|---------------|---------------------|
| **Automatic oil control** | ✅ Yes | ✅ Yes | ✅ Yes |
| **System controller integration (RS485)** | ❌ No | ✅ Yes (Modbus RTU) | ✅ Yes (Modbus RS485) |
| **BMS/SCADA integration** | ❌ No | ⚠️ Limited (serial only) | ✅ Yes (full) |
| **Field configuration** | ⚠️ DIP switches | ❌ No (factory only) | ✅ Yes (NFC wireless) |
| **Remote monitoring** | ❌ No | ✅ Yes (serial) | ✅ Yes (RS485) |
| **Data logging** | ❌ No | ✅ Yes (via controller) | ✅ Yes (via BMS) |
| **Predictive maintenance** | ❌ No | ✅ Yes (serial tracking) | ✅ Yes (full tracking) |
| **Cost** | Lowest | Medium (~30% less than TK4) | Highest (NFC premium) |
| **Recommended when** | Basic automatic control | System controller RS485 | BMS/SCADA + field config |

---

## 7. INSTALLATION & SERVICE

### 7.1 Mounting Requirements

**Clearances:**
- **Above**: 120-150mm (for electronic module removal during service)
- **Sides**: 80mm (for cable/piping access, wiring)
- **Below**: 30mm minimum (glass dome immersion depth)

**Flange Adapters:**
- Adapters sold separately (not included with TK4 MB)
- Select adapter matching compressor flange type:
  - 3-hole sight-glass flange
  - 4-hole sight-glass flange
  - 6-hole sight-glass flange
- See Teklab Adapters Addendum for selection guide
- Same adapters as TK3+/TK4 series (interchangeable)

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
- Fuse protection:
  - 1A slow-blow for TK4 MB 46 bar (20VA)
  - 2A slow-blow for TK4 MB 80/130 bar (30VA)

**Relay Wiring (Safety Chain):**
- Use NC contact in series with compressor contactor coil
- Wire gauge: 1.0-1.5 mm² (18-14 AWG) for 230VAC @ 2A
- NC contact: Closed during normal operation → Opens on alarm
- Typical wiring: NC contact interrupts compressor contactor supply

**Modbus RTU RS485 Wiring:**
- Use twisted pair cable (Belden 3105A or equivalent)
- Wire gauge: 0.5-0.75 mm² (22-18 AWG)
- Daisy-chain topology (not star)
- Polarity: A+ and B- (mark cables to avoid reversal)
- Install 120Ω termination resistors at both ends of network
- Maximum cable length: 1200m
- Maximum devices per network: 32 (without repeaters)

**Multi-Compressor Systems:**
- Wire all TK4 MB relay NC contacts in **series** (safety chain)
- Any unit alarm → stops all compressors
- Modbus RTU network: Daisy-chain all TK4 MB units to system controller
- Verify unique Modbus address for each TK4 MB (factory-configured)

### 7.3 Modbus RTU RS485 Network Setup

**Physical Wiring:**
1. Connect twisted pair from system controller to first TK4 MB (A+, B-)
2. Daisy-chain from first TK4 MB to second TK4 MB (continue for all units)
3. Install 120Ω terminator at system controller
4. Install 120Ω terminator at last TK4 MB in chain
5. Verify polarity (A+ to A+, B- to B-)

**System Controller Configuration:**
1. Configure controller Modbus RTU parameters:
   - Baud rate: 9600 bps (or match factory-configured rate)
   - Data format: 8N1 (or match factory-configured format)
2. Add Modbus devices (TK4 MB addresses as factory-configured)
3. Import TK4 MB register map (available from Teklab)
4. Configure polling rate (1-5 seconds per device)
5. Test communication (verify each TK4 MB responds)

**Factory Address Verification:**
- Each TK4 MB ships with unique Modbus address (specified at order)
- Verify address label on unit matches system controller configuration
- No field programming required (plug-and-play)

### 7.4 Commissioning

**Pre-Startup Checklist:**
1. Verify power supply voltage matches TK4 MB rating (24VAC or 230VAC)
2. Check all electrical connections secure (power, relay, Modbus RTU)
3. Verify oil return line connected and isolation valve open
4. Confirm relay wiring correct (NC contact in series with contactor)
5. Verify adequate oil in separator
6. Verify Modbus RTU RS485 termination resistors installed (both ends)
7. Test Modbus RTU communication (system controller can read each TK4 MB address)
8. Verify factory-configured Modbus address matches system controller configuration

**Initial Startup:**
1. Power on TK4 MB units
2. Observe LED indication (should show red initially if crankcase empty)
3. Verify system controller can read Modbus RTU data (oil level status, valve state)
4. Start compressor system
5. TK4 MB valve opens automatically (yellow LED, valve state OPEN in controller)
6. Oil fills crankcase to setpoint
7. TK4 MB valve closes (green LED, valve state CLOSED in controller)
8. Monitor for 30 minutes to verify stable operation
9. Log Modbus RTU data for baseline (operating hours, valve cycles)

**LED Indication:**
- **Green**: Normal operation (oil level adequate, valve closed)
- **Yellow**: Filling mode (oil level low, valve open, oil flowing)
- **Red**: Alarm (oil level low despite valve open for 60-120 sec)

### 7.5 Service & Maintenance

**Routine Maintenance:**
- **Quarterly**: Visual inspection (check for leaks, verify LED indication, review Modbus RTU data)
- **Annually**: Functional test (verify valve operation, relay output, Modbus RTU communication)
- **No scheduled component replacement** (replace only if failed)

**Remote Monitoring via Modbus RTU:**
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
7. **Verify factory-configured Modbus address** (module retains configuration)
8. Verify Modbus RTU communication restored

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
9. **Verify factory-configured Modbus address** (new unit must match system controller)
10. Evacuate and test for leaks
11. Return to service
12. Verify Modbus RTU communication

### 7.6 Troubleshooting

**Alarm Activates Immediately After Startup:**
- **Cause**: Oil separator empty or pressure too low
- **Solution**: Verify separator oil level, check separator pressure adequate (> 5 bar above crankcase)
- **Modbus RTU Check**: Read valve state (should be OPEN if level low)

**Valve Won't Open (Red LED, no oil flow):**
- **Cause**: Coil failure, wiring issue, insufficient differential pressure
- **Solution**: Check power supply, verify coil voltage, measure MOPD (need > 5 bar minimum)
- **Modbus RTU Check**: Read valve state (should show OPEN command, verify coil energized)

**Continuous Filling (Yellow LED stays on):**
- **Cause**: Oil return line restricted, valve stuck open
- **Solution**: Check for blockage, verify line sizing adequate, inspect valve seat
- **Modbus RTU Check**: Read valve cycle counter (abnormal cycle frequency indicates issue)

**False Alarms (Intermittent Red LED):**
- **Cause**: Foam in crankcase, low refrigerant charge, undersized oil separator
- **Solution**: Check refrigerant charge, verify separator size adequate, check for liquid slugging
- **Modbus RTU Check**: Review alarm history (pattern analysis for root cause)

**No LED Indication:**
- **Cause**: Power supply failure, electronic module failure
- **Solution**: Verify power supply voltage at terminals, check fuse, replace module if needed
- **Modbus RTU Check**: Verify system controller cannot communicate (confirms module failure)

**Modbus RTU Communication Failure:**
- **Cause**: Wiring issue, termination missing, address conflict, wrong baud rate
- **Solution**: Check twisted pair continuity, verify 120Ω terminators installed, verify unique factory-configured addresses, verify baud rate matches system controller
- **Factory Address Check**: Verify address label on unit matches system controller configuration

---

## 8. FREQUENTLY ASKED QUESTIONS (FAQ)

### 8.1 Product Classification & Comparison

**Q1: What is the main difference between TK4 MB and TK4 (standard)?**

**TK4 MB** = Modbus RTU serial only (factory-configured):
- Modbus RTU RS485 serial communication
- Factory-configured (no field programming)
- Plug-and-play serial connectivity
- Lower cost (~30% less than TK4 standard)

**TK4 (standard)** = Modbus RS485 + NFC wireless:
- Both Modbus RS485 and NFC wireless configuration
- Field-programmable via smartphone/tablet
- On-site parameter adjustments
- Higher cost (NFC hardware included)

**Choose TK4 MB when**: System controller integration via RS485, factory-configured operation preferred, cost priority

**Choose TK4 standard when**: BMS/SCADA integration required, field programmability essential

**Q2: What is the difference between TK4 MB and TK3+?**

**Main difference: Configuration and connectivity**
- **TK3+**: DIP switches for configuration, NO communication (standalone only)
- **TK4 MB**: Modbus RTU RS485 serial communication, factory-configured

**TK4 MB features vs TK3+:**
- Modbus RTU for system controller integration
- Remote monitoring and data logging
- Factory-configured operation
- ~50-60% higher cost

**What's identical:**
- Same IR optical sensor technology
- Same pressure ratings (46/80/130 bar)
- Same automatic valve and installation

**Choose TK3+ when**: Basic automatic control, no communication, cost priority  
**Choose TK4 MB when**: System controller RS485 integration required, serial monitoring needed

**Q3: Is TK4 MB a regulator or level switch?**
TK4 MB is a complete **oil level regulator** (not just a level switch). It combines electro-optic level detection with integrated solenoid valve and control electronics for automatic oil level regulation. Modbus RTU serial adds monitoring capability but does not change core function.

### 8.2 Connectivity & Configuration

**Q4: How do I configure TK4 MB without NFC?**

**Factory Default Settings**: TK4 MB ships pre-configured, operates plug-and-play:
- Default Modbus address (specified at order)
- Default baud rate (typically 9600 bps)
- Default setpoints for oil level control

**Parameter Changes**: Requires factory service:
- Contact Teklab for configuration change
- Or order with custom factory configuration
- No on-site field programming available

TK4 MB designed for fixed installations where parameters rarely change.

**Q5: How do I set up Modbus RTU RS485 on TK4 MB?**

**Wiring:**
- Connect twisted pair to RS485 terminals (A+, B-)
- Daisy-chain multiple units
- Install 120Ω terminators at both ends
- Max 1200m cable length

**Addressing:**
- Each TK4 MB has unique factory-configured Modbus address (1-247)
- Verify address label on unit matches system controller configuration

**System Controller Integration:**
- Configure controller with TK4 MB addresses
- Import register map
- Poll for oil level status/valve state/alarms/operating hours

**Baud Rate:**
- Typically 9600 bps (factory default)
- Higher rates (19200/38400 bps) available via custom order

**Q6: What data can I read via Modbus RTU?**
- Oil level status (OK / LOW / ALARM)
- Valve state (OPEN / CLOSED)
- Alarm status and history
- Operating hours (sensor and valve)
- Valve cycle counter (predictive maintenance)
- Module temperature
- Configuration parameters (read-only)

Typical polling rate: 1-5 seconds per unit.

**Q7: Can I adjust setpoints remotely via Modbus RTU?**
No. Setpoint adjustment **requires factory service or replacement**:
- Modbus RTU: Read-only access to configuration
- No field programming capability (factory-configured only)
- Prevents accidental parameter changes

**For field-adjustable setpoints, choose TK4 standard with NFC.**

**Q8: Can I use TK4 MB without Modbus RTU?**
Yes. TK4 MB works standalone:
- Leave RS485 terminals unconnected if Modbus RTU not needed
- Factory default settings work for most applications
- Future-proof: add serial connectivity later without hardware replacement

**If connectivity never needed, TK3+ more cost-effective.**

### 8.3 Operation & Installation

**Q9: Does TK4 MB require external controllers?**
No. TK4 MB operates automatically out-of-box (plug-and-play):
- Factory-configured for immediate operation
- Self-contained sensor + valve + control
- Modbus RTU serial is optional enhancement (not required for basic operation)
- Operates identically to TK3+ for automatic oil level control

**Q10: What adapters are compatible with TK4 MB?**
TK4 MB uses same adapters as TK3+/TK4 series:
- Bitzer, Copeland, Frascold, Dorin, Bock compressor adapters
- 3-hole, 4-hole, 6-hole flange adapters
- Sight-glass replacement mounting

Order adapters separately. Specify compressor brand/model when ordering.

**Q11: Can TK4 MB replace existing TK3+ or TK4 units?**
Yes, drop-in replacement:
- Identical dimensions (108.25mm H × 59.5mm W)
- Same adapters, flanges, voltage options (24VAC/230VAC)
- Power consumption: TK4 MB 46 bar = 20VA (same as TK3+), TK4 MB 80/130 bar = 30VA
- Retrofit: Remove old unit, install TK4 MB on existing adapter, add Modbus RTU wiring

### 8.4 Pressure & Applications

**Q12: What does MOPD mean?**
MOPD = **Maximum Operating Pressure Differential** (separator pressure minus crankcase pressure).

**TK4 MB Variants:**
- TK4 MB 46 bar: MOPD 26 bar
- TK4 MB 80 bar: MOPD 60 bar
- TK4 MB 130 bar: MOPD 100 bar

**Calculation:** Separator pressure - Crankcase pressure ≤ MOPD rating

**Example:** 28 bar separator - 3 bar crankcase = 25 bar differential (OK for TK4 MB 46 bar)

**Q13: Which TK4 MB variant for CO2 systems?**
- **CO2 subcritical** (differential 30-60 bar): TK4 MB 80 bar
- **CO2 transcritical** (differential 60-100 bar): TK4 MB 130 bar

**Note:** CO2 systems with system controller (TK4 MB ideal choice for RS485 integration).

**Q14: Can TK4 MB 46 bar be used for CO2?**
No, CO2 exceeds MOPD 26 bar:
- CO2 subcritical: 40-60 bar differential → Use TK4 MB 80 bar
- CO2 transcritical: 70-100 bar differential → Use TK4 MB 130 bar

**TK4 MB 46 bar suitable for**: R134a, R404A, R407C, R410A (standard conditions), all systems with differential < 26 bar.

**Q15: R410A hot climate - which TK4 MB model?**
R410A at 50°C condensing creates ~30 bar differential. Use **TK4 MB 80 bar** for safety margin (MOPD 60 bar). TK4 MB 46 bar works but operates at maximum rating (less safe).

### 8.5 Service & Troubleshooting

**Q16: How do I replace the TK4 MB module?**
1. Disconnect power
2. Remove mounting screws
3. Lift off module
4. Install new module
5. Reconnect power
6. Verify factory-configured Modbus address retained

**Time:** 5-10 minutes, no refrigerant recovery needed.

**Q17: What maintenance is required?**
- **Quarterly**: Visual inspection, review Modbus RTU data (valve cycles, alarms)
- **Annually**: Functional test (verify valve operation, relay output, communication)
- **No scheduled component replacement** (only replace if failed)

**Predictive maintenance via Modbus RTU**: Monitor valve cycle counter for early failure detection.

**Q18: How to troubleshoot Modbus RTU communication failure?**
- Check twisted pair continuity
- Verify 120Ω terminators installed at both ends
- Verify unique factory-configured addresses (no conflicts)
- Verify baud rate matches system controller (typically 9600 bps)
- Check factory address label on unit

**Q19: Can I change Modbus address in the field?**
No. TK4 MB is factory-configured:
- Address programmed at factory (specified at order)
- No field programming capability
- Address change requires factory service or replacement

**For field-adjustable address, choose TK4 standard with NFC.**

**Q20: Can I upgrade TK3+ to TK4 MB serial connectivity?**
No. Hardware is different (TK4 MB has Modbus RTU board integrated). However:
- Same mounting footprint (drop-in replacement)
- Same adapters compatible
- Retrofit process: Remove TK3+, install TK4 MB, add Modbus RTU wiring

---

## 9. ORDERING INFORMATION

### 9.1 Product Code Structure

**Format**: `TK4MB-[Pressure]-[Voltage]-[Cable Type]-[Cable Length]-[Modbus Address]`

**Example**: `TK4MB-46-230VAC-CON-3M-ADDR001`
- TK4 MB series (Modbus RTU serial)
- 46 bar max pressure variant
- 230VAC power supply
- Connector type (EN175301-803)
- 3 meter cable length
- Modbus address 001 (factory-configured)

### 9.2 Selection Options

**Pressure Variant:**
- `46` = TK4 MB 46 bar (MOPD 26 bar, 20VA)
- `80` = TK4 MB 80 bar (MOPD 60 bar, 30VA)
- `130` = TK4 MB 130 bar (MOPD 100 bar, 30VA)

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

**Modbus Address (Factory-Configured):**
- `ADDR001` to `ADDR247` = Unique Modbus address (specify at order)
- Default: ADDR001 (if not specified)

**Custom Baud Rate (Optional):**
- Default: 9600 bps (if not specified)
- Custom: 19200 or 38400 bps (specify at order)

### 9.3 Accessories (Sold Separately)

**Required:**
- **Adapter**: TK4 MB requires an adapter to mount to compressor flange (3/4/6-hole types). See Teklab Adapters Addendum.

**Optional:**
- **RS485 Termination Resistors**: 120Ω (required at both ends of network)
- **Twisted Pair Cable**: Belden 3105A or equivalent for RS485 network

---

## 10. CONNECTIVITY FEATURES (MODBUS RTU + NFC NANO INTERFACE)

### 10.1 Dual Communication Architecture Overview

The **TK4 MB Series** features a revolutionary **dual communication architecture** combining:

1. **Modbus RTU Serial (RS485)** - Wired continuous communication for remote monitoring and integration with BMS/SCADA systems
2. **NFC Nano Interface** - Wireless proximity configuration via TK4-PRG-NANO dongle for local setup and diagnostics

**Key Advantage**: The dual approach allows **continuous remote monitoring** (via RS485 Modbus network) while enabling **easy local configuration** (via NFC wireless through plastic enclosures) without opening electrical panels.

**Architecture Differentiators:**
- **TK4 MB**: Modbus RTU + NFC (this model) - Full remote monitoring + local wireless configuration
- **TK4 Standard**: Modbus RS485 + NFC - Both protocols available (see TK4 Series documentation)
- **TK3 Standard**: DIP switches only - No connectivity features

---

### 10.2 Modbus RTU Communication (Wired RS485)

#### 10.2.1 Protocol Overview

**Function**: Continuous real-time communication with BMS/SCADA/PLC systems via RS485 serial network.

**Protocol Specifications:**
- **Standard**: Modbus RTU (binary encoding)
- **Physical Layer**: RS485 half-duplex (2-wire or 4-wire)
- **Network Topology**: Multi-drop bus (up to 32 devices per segment)
- **Baud Rate**: 9600 bps (default), 19200 bps, 38400 bps (configurable via NFC or factory order)
- **Parity**: Even (default), None, Odd (configurable via NFC)
- **Data Bits**: 8
- **Stop Bits**: 1 (parity enabled), 2 (no parity)
- **Slave Address**: 1-247 (configurable via NFC or factory order)
- **Cable Distance**: Up to 1200m (4000 ft) per segment with proper cabling

**Node Configuration:**
- TK4 MB operates as **Modbus slave** (responds to master requests)
- Master device: BMS/SCADA/PLC/controller (user-provided)
- Multiple TK4 MB units can share same RS485 bus (unique addresses required)

#### 10.2.2 RS485 Wiring

**Physical Connection:**
- **2-Wire Configuration** (typical): A(+), B(-), GND (shield ground)
- **Cable Type**: Twisted pair shielded cable (Belden 3105A or equivalent)
- **Wire Gauge**: 18-22 AWG (0.75-1.5 mm²)
- **Termination**: 120Ω resistor at both network ends (first/last device)

**TK4 MB Terminal Block:**
- **RS485-A (+)**: Yellow wire or A+ terminal
- **RS485-B (-)**: White wire or B- terminal
- **GND**: Shield ground (connect at one point only to avoid ground loops)

**Multi-Drop Wiring:**
```
Master (BMS/PLC)
    ├── RS485 A/B ──[120Ω]──┬── TK4 MB #1 (Addr 1)
                            ├── TK4 MB #2 (Addr 2)
                            ├── TK4 MB #3 (Addr 3)
                            └── TK4 MB #N (Addr N) ──[120Ω]
```

**Termination Resistor Locations:**
- **First device**: At master (BMS/PLC) or first TK4 MB
- **Last device**: At last TK4 MB unit in network
- **Middle devices**: No termination resistors

#### 10.2.3 Modbus Register Map

**Read-Only Registers (Function Code 03 - Read Holding Registers):**

| Register Address | Parameter | Data Type | Unit | Description |
|-----------------|-----------|-----------|------|-------------|
| 40001 | Valve Status | Boolean | - | 0=Closed, 1=Open |
| 40002 | Alarm Status | Boolean | - | 0=Normal, 1=Alarm Active |
| 40003 | Cycle Counter | Uint16 | cycles | Total valve openings (0-65535) |
| 40004 | Oil Level Status | Boolean | - | 0=Low, 1=OK |
| 40005 | Sensor Fault | Boolean | - | 0=OK, 1=Fault Detected |
| 40006 | Power On Time | Uint32 (2 registers) | hours | Total operating time |
| 40008 | Firmware Version | Uint16 | - | e.g. 0x0120 = v1.20 |
| 40009 | Device Model | Uint16 | - | 46=TK4 MB 46 bar, 80=80 bar, 130=130 bar |

**Write Registers (Function Code 06 - Write Single Register / Function Code 16 - Write Multiple Registers):**

| Register Address | Parameter | Data Type | Range | Description |
|-----------------|-----------|-----------|-------|-------------|
| 40101 | Alarm Reset | Boolean | 0-1 | Write 1 to clear alarm (auto-resets to 0) |
| 40102 | Manual Override | Boolean | 0-1 | 0=Auto, 1=Manual Valve Open |
| 40103 | Cycle Counter Reset | Boolean | 0-1 | Write 1 to reset counter to 0 |

**Example Modbus Read Request (Read Valve Status):**
```
Master Request: [Addr 01] [Function 03] [Start Reg 40001] [Qty 1] [CRC]
Slave Response: [Addr 01] [Function 03] [Byte Count 02] [Data 00 01] [CRC]
Interpretation: Valve Status = 1 (Open)
```

**Example Modbus Write Request (Reset Alarm):**
```
Master Request: [Addr 01] [Function 06] [Reg 40101] [Value 00 01] [CRC]
Slave Response: [Addr 01] [Function 06] [Reg 40101] [Value 00 01] [CRC]
Result: Alarm cleared
```

#### 10.2.4 SCADA/BMS Integration

**Typical Integration Workflow:**

1. **Network Setup**: Wire all TK4 MB units to RS485 bus with unique addresses
2. **Master Configuration**: Add TK4 MB devices to BMS/SCADA node list (specify address, baud rate)
3. **Polling Setup**: Configure master to poll registers at desired interval (e.g., every 5 seconds)
4. **Alarm Mapping**: Map register 40002 (Alarm Status) to BMS alarm system
5. **Dashboard Display**: Display valve status (40001), cycle count (40003), oil level (40004) on SCADA HMI
6. **Historical Logging**: Log cycle counter and alarm events for predictive maintenance

**Common SCADA Systems:**
- **Carel pCOWeb**: Add TK4 MB as Modbus RTU slave, configure registers in device template
- **Danfoss AK-SM**: Use Modbus RTU driver, map registers to AK controller variables
- **Honeywell Tridium**: Create Modbus RTU driver, link registers to Niagara points
- **Generic OPC/SCADA**: Use Modbus RTU driver with register addresses above

**Monitoring Parameters:**
- **Real-Time**: Valve open/close status, oil level OK/low, active alarms
- **Diagnostics**: Cycle counter (wear tracking), sensor fault detection
- **Historical**: Cycle count trends (predict valve replacement), alarm frequency analysis

#### 10.2.5 Network Architecture Best Practices

**Single Segment (Up to 32 Devices, 1200m):**
- Use proper twisted pair cable (Belden 3105A or equivalent)
- Install 120Ω termination at both network ends
- Keep cable runs straight (avoid star/branch topologies)
- Shield ground at master end only (avoid ground loops)

**Multiple Segments (More than 32 Devices):**
- Use RS485 repeaters between segments (isolates segments, regenerates signal)
- Each segment supports up to 32 devices
- Total network: Up to 247 devices with repeaters

**Cable Installation:**
- Avoid running RS485 cable parallel to high-voltage AC power cables
- Cross AC cables at 90° angle if unavoidable
- Use shielded twisted pair cable throughout
- Keep cable runs away from variable frequency drives (VFDs) and motors

---

### 10.3 NFC Nano Interface (Wireless Local Configuration)

#### 10.3.1 Overview

**Function**: Wireless proximity configuration and diagnostics via **TK4-PRG-NANO USB dongle** connected to Windows PC or Android device.

**Key Advantages Over Traditional Interfaces:**
- **No Physical Connection Required**: Configure through plastic enclosures (5-10 cm proximity)
- **No Electrical Panel Opening**: Technician stays outside hazardous electrical zones
- **Extremely Fast Setup**: 30 seconds typical configuration time vs. 5-10 minutes with DIP switches
- **User-Friendly App**: Intuitive GUI vs. cryptic DIP switch manuals
- **Future-Proof**: App updates add new features without hardware changes

**Operating Principle:**
- NFC (Near Field Communication) ISO 14443 at 13.56 MHz
- Wireless power transfer allows configuration even when TK4 MB is unpowered
- Bidirectional data exchange (read/write parameters)

#### 10.3.2 Hardware Components

**TK4-PRG-NANO Dongle (Sold Separately):**
- **Interface**: USB 2.0 Type-A connector
- **Cable**: 1.5m USB extension cable (allows flexible positioning)
- **Antenna**: Integrated 13.56 MHz NFC coil
- **Dimensions**: 85 × 55 × 12 mm (compact credit-card size)
- **Operating Range**: 5-10 cm (2-4 inches) from TK4 MB unit
- **Weight**: 45g
- **LED Indicators**: Power (blue), NFC Activity (green), Error (red)
- **Operating Temp**: -10°C to +50°C
- **Price**: Approx. €100-150 (one-time purchase, reusable for all TK4/TK4 MB units)

**Compatible Devices:**
- **Windows**: Windows 7/8/10/11 (USB 2.0 port required)
- **Android**: Android 5.0+ with USB OTG support (USB-C adapter may be required)
- **iOS**: Not supported (Apple restricts USB host mode)

**TK4 MB NFC Antenna Location:**
- Integrated inside TK4 MB housing (no external connector)
- Optimal positioning: Place dongle flat against TK4 MB body near label
- **Works through plastic**: Effective through standard IP65 plastic enclosures up to 5mm thick
- **Does not work through metal**: Metal enclosures block NFC (use external NFC antenna if needed)

#### 10.3.3 Software Application

**TK4 Configuration App (Free Download):**
- **Platform**: Windows .exe installer, Android APK via Google Play Store
- **Download**: www.teklab.com/downloads → TK4 Series → TK4 Configuration App
- **License**: Free (no subscription fees)
- **Updates**: Automatic over internet (new features added regularly)
- **Languages**: English, Italian, German, French, Spanish (auto-detects Windows/Android locale)
- **File Size**: ~15 MB (Windows), ~8 MB (Android)

**App Features:**
- **Parameter Configuration**: Set all TK4 MB parameters (see Section 10.4)
- **Real-Time Monitoring**: View valve status, cycle counter, alarm status (live refresh)
- **Diagnostics**: Read alarm history, sensor test results, firmware version
- **Profile Management**: Save/load configuration profiles (standardize multi-unit installations)
- **Firmware Updates**: Update TK4 MB firmware via NFC (when available)
- **Help System**: Context-sensitive help, parameter tooltips, quick start wizard

**User Interface:**
- **Dashboard**: Real-time valve status, oil level, cycle counter, alarms
- **Configuration Tabs**: Basic Functioning, Advanced, Modbus, Security
- **Toolbar**: Connect, Read, Write, Save Profile, Load Profile, Help
- **Status Bar**: Connection status, last action, NFC signal strength

#### 10.3.4 Operating Modes

**1. Powered Operation (TK4 MB Energized):**
- **Power Source**: TK4 MB powered by 24VAC or 230VAC supply
- **Functionality**: Full read/write access to all parameters
- **Real-Time Monitoring**: Live valve status, sensor readings, alarm status
- **Speed**: Fast parameter transfer (<1 second per parameter)
- **Use Case**: Field adjustments during commissioning or troubleshooting with system running

**2. Unpowered Operation (TK4 MB De-Energized):**
- **Power Source**: Wireless power transfer from NFC dongle (harvested energy)
- **Functionality**: Basic configuration only (cannot monitor live status)
- **Parameters Available**: All configuration parameters (valve timings, alarms, Modbus settings)
- **Speed**: Slower parameter transfer (~3-5 seconds per parameter due to power harvesting)
- **Use Case**: Workshop pre-configuration before installation, or field configuration with power lockout

**Advantages:**
- **Safety**: Configure in unpowered mode during maintenance lockout (LOTO compliance)
- **Flexibility**: Pre-configure units in workshop before shipping to site
- **Convenience**: No need to energize TK4 MB for basic parameter setup

#### 10.3.5 Configuration Parameters (via NFC)

**Parameters Accessible via Nano Interface:**

**Basic Functioning:**
- Sensor mode selection (normally high / normally low)
- Valve opening delay (0-255 seconds, factory default 15s)
- Valve closing delay (0-255 seconds, factory default 15s)
- Minimum cycle time (anti-short-cycle protection, 30-600 seconds, default 120s)

**Advanced Parameters:**
- Alarm enable/disable (sensor fault, valve stuck, cycle count threshold)
- Alarm delay (time before alarm activation, 1-60 seconds, default 5s)
- Cycle counter reset (manual reset or scheduled auto-reset)
- Power-on state (valve default open/closed after power loss)

**Modbus Configuration:**
- **Slave address** (1-247, default 1) - Critical for multi-drop networks
- **Baud rate** (9600, 19200, 38400 bps, default 9600)
- **Parity** (Even, None, Odd, default Even)
- **Response delay** (time before slave responds, 0-250ms, default 10ms)

**Security:**
- **Password protection** (enable/disable access control)
- **Password change** (4-8 digit PIN)
- **Access log** (last 10 configuration changes with timestamps)

**Diagnostics (Read-Only):**
- Firmware version (e.g., v1.25)
- Serial number (unique device ID)
- Total operating hours (power-on time)
- Cycle counter (total valve openings)
- Last alarm code (fault identification)
- NFC access count (number of configuration sessions)

#### 10.3.6 Typical Configuration Workflows

**Workflow 1: Initial Commissioning (Workshop Pre-Configuration + Site Installation)**

**Phase A - Workshop (Unpowered Mode):**
1. Open TK4 Configuration App on Windows PC
2. Connect TK4-PRG-NANO dongle to USB port (wait for blue LED)
3. Place TK4 MB unit on desk (unpowered), position dongle on body
4. Click "Connect" → App detects TK4 MB via NFC (green LED flashes)
5. Navigate to "Basic Functioning" tab:
   - Set valve opening delay: 15s
   - Set valve closing delay: 15s
   - Set minimum cycle time: 120s
6. Navigate to "Modbus" tab:
   - Set slave address: 5 (for unit #5 in network)
   - Set baud rate: 9600 bps
   - Set parity: Even
7. Navigate to "Security" tab:
   - Enable password protection: Yes
   - Set password: 1234 (customer-specific)
8. Click "Write All" → App transfers parameters to TK4 MB (~20 seconds)
9. Click "Save Profile" → Save as "Customer_Site_Standard.tkp"
10. Repeat for remaining units (use "Load Profile" → "Write All" for fast duplication)

**Phase B - Site (Powered Mode):**
1. Install TK4 MB units on compressors (mount adapters, wire RS485, wire power)
2. Energize system (apply 24VAC or 230VAC to TK4 MB units)
3. Connect dongle to TK4 MB #5 through plastic panel (no opening required)
4. Click "Connect" → View real-time dashboard:
   - Valve status: Closed (initial state)
   - Oil level: Low (compressor just started)
   - Cycle counter: 0
5. Monitor for 10 minutes → Confirm valve opens when oil level drops (valve status: Open)
6. Verify Modbus communication: BMS/SCADA displays TK4 MB #5 data correctly
7. Repeat verification for other units
8. Disconnect dongle → Installation complete

**Workflow 2: Field Optimization (Adjust Cycle Timings)**

**Scenario**: Customer reports excessive valve cycling (valve opens/closes too frequently).

1. Connect dongle to problematic TK4 MB through plastic panel (powered mode)
2. Click "Connect" → Read current configuration:
   - Valve opening delay: 15s (factory default)
   - Valve closing delay: 15s (factory default)
   - Minimum cycle time: 120s (factory default)
3. Review diagnostics:
   - Cycle counter: 450 cycles (in 24 hours = excessive)
4. Adjust parameters to reduce cycling:
   - **Increase valve opening delay**: 15s → 30s (slower response)
   - **Increase minimum cycle time**: 120s → 180s (prevents rapid re-opening)
5. Click "Write" → Transfer new parameters
6. Monitor for 24 hours → Cycle count drops to 180 cycles (50% reduction)
7. Save optimized profile: "Site_Low_Cycling_Profile.tkp"
8. Load profile to other units if needed

**Workflow 3: Troubleshooting (Alarm Diagnostics)**

**Scenario**: BMS reports alarm from TK4 MB #12 (Modbus register 40002 = 1).

1. Connect dongle to TK4 MB #12 through plastic panel
2. Click "Connect" → Navigate to "Diagnostics" tab:
   - Last alarm code: "Sensor Fault" (code 03)
   - Alarm timestamp: 2025-11-15 14:32:18
   - Cycle counter: 1250 cycles (normal)
3. Perform sensor test:
   - App sends test command → TK4 MB activates IR LED, reads sensor
   - Result: "Sensor response abnormal" (contamination detected)
4. Maintenance action: Clean sight glass window with isopropyl alcohol
5. Clear alarm: Click "Alarm Reset" button → Alarm clears (Modbus register 40002 = 0)
6. Re-test sensor: Click "Sensor Test" → Result: "Sensor response normal"
7. Monitor for 1 hour → No alarm recurrence → Issue resolved
8. Log action in maintenance record: "TK4 MB #12 sensor cleaned, alarm cleared"

**Workflow 4: Multi-Unit Standardization (Profile Save/Load)**

**Scenario**: Install 20 TK4 MB units with identical configuration.

1. Configure first unit with desired parameters (Workflow 1 Phase A)
2. Click "Save Profile" → Save as "Standard_20Units.tkp"
3. For units #2-20:
   - Connect dongle to unit
   - Click "Load Profile" → Select "Standard_20Units.tkp"
   - Modify only unique parameter: Modbus slave address (2, 3, 4, ... 20)
   - Click "Write All" → Transfer parameters (~20 seconds)
   - Disconnect and move to next unit
4. Total time: ~10 minutes for 20 units (vs. 3+ hours with manual DIP switch configuration)

#### 10.3.7 Security Features

**Password Protection:**
- **Purpose**: Prevent unauthorized configuration changes
- **Activation**: Enable in "Security" tab → Set 4-8 digit PIN
- **Effect**: NFC connection requires password entry before write access granted
- **Bypass**: Read-only access (monitoring) allowed without password
- **Factory Reset**: Available via hardware jumper (requires opening TK4 MB - intentionally difficult)

**Access Logging:**
- **Function**: Records last 10 configuration sessions
- **Data Logged**: Date/time, parameter changes, user ID (optional)
- **Purpose**: Audit trail for troubleshooting or compliance
- **Retrieval**: View in "Diagnostics" → "Access Log" tab

**Physical Security:**
- **Limited Range**: 5-10 cm proximity required (prevents remote hacking)
- **NFC Standard**: ISO 14443 with encryption (prevents eavesdropping)
- **No Wireless Broadcasting**: TK4 MB does not transmit without dongle present (passive NFC tag)

**Best Practices:**
- **Workshop**: No password required (pre-configuration convenience)
- **Site Installation**: Enable password after commissioning (prevent tampering)
- **Password Management**: Store password in secure location (e.g., customer documentation, password manager)
- **Physical Access Control**: Restrict dongle access to authorized personnel only

#### 10.3.8 Technical Specifications (NFC System)

**NFC Communication:**
- **Standard**: ISO 14443 Type A
- **Frequency**: 13.56 MHz (ISM band, license-free worldwide)
- **Modulation**: ASK (Amplitude Shift Keying)
- **Data Rate**: 106 kbps (parameter transfer), 424 kbps (firmware updates)
- **Range**: 5-10 cm (2-4 inches) typical, dependent on enclosure material
- **Power Transfer**: Inductive coupling (wireless power to TK4 MB in unpowered mode)
- **Encryption**: AES-128 (password protection mode)

**TK4-PRG-NANO Dongle:**
- **Interface**: USB 2.0 Type-A (backwards compatible USB 1.1)
- **Power Consumption**: 150 mA @ 5V (0.75W) typical
- **Cable Length**: 1.5m USB extension (allows flexible positioning)
- **Antenna**: 50mm diameter coil (optimized for 13.56 MHz)
- **Dimensions**: 85 × 55 × 12 mm (credit card size)
- **Weight**: 45g
- **Housing**: ABS plastic (IP40 indoor use)
- **LED Indicators**:
  - **Blue**: USB power connected
  - **Green**: NFC communication active (flashing)
  - **Red**: Error (connection failed, device not found)
- **Certifications**: CE, FCC, RoHS compliant

**Barrier Penetration:**
- **Plastic**: Effective through ABS, polycarbonate, acrylic up to 5mm thick (typical IP65 enclosures)
- **Glass**: Effective through glass up to 3mm (sight glass windows)
- **Metal**: **NOT effective** through metal enclosures (aluminum, steel) - use external NFC antenna if needed
- **Air Gap**: Maximum 10 cm in free air (no obstructions)

**Operating Environment:**
- **Temperature**: -10°C to +50°C (dongle), -40°C to +70°C (TK4 MB NFC antenna)
- **Humidity**: 10-90% RH non-condensing (dongle), 100% RH (TK4 MB IP65 sealed)
- **Altitude**: 0-3000m AMSL
- **EMC**: CE EMC Directive 2014/30/EU compliant (immune to industrial EMI)

#### 10.3.9 Ordering Information (NFC System)

**TK4-PRG-NANO Package (Sold Separately):**
- **Part Number**: TK4-PRG-NANO
- **Description**: NFC configuration dongle for TK4/TK4 MB series
- **Package Includes**:
  - TK4-PRG-NANO USB dongle with 1.5m cable
  - Quick Start Guide (printed card)
  - Download link for TK4 Configuration App (Windows/Android)
- **Price**: Approx. €100-150 (one-time purchase)
- **Compatibility**: All TK4 and TK4 MB models (46/80/130 bar, 24VAC/230VAC)
- **Reusability**: One dongle configures unlimited TK4/TK4 MB units (lifetime use)

**Software (Free):**
- **TK4 Configuration App**: Free download from www.teklab.com/downloads
- **License**: No subscription fees, no activation codes required
- **Updates**: Automatic over internet (new features added regularly)

**Optional Accessories:**
- **USB-C to USB-A Adapter**: For Android devices without USB-A port (~€5)
- **External NFC Antenna**: For metal enclosures (special order, ~€50)

#### 10.3.10 Integration of NFC with Modbus RTU Operation

**Relationship Between NFC and Modbus RTU:**

**Independent Interfaces:**
- NFC and Modbus RTU operate **independently** - configuration via NFC does not disrupt Modbus communication
- TK4 MB continues normal Modbus slave operation while NFC session active
- BMS/SCADA can poll Modbus registers simultaneously with NFC configuration

**Configuration Priority:**
- **NFC writes take effect immediately** - new parameters applied to TK4 MB as soon as "Write" button clicked
- **Modbus master sees updated values** - e.g., if slave address changed via NFC, Modbus master must update node list
- **No Modbus write conflicts** - NFC has exclusive write access to configuration registers (Modbus read-only for config)

**Typical Combined Workflow:**
1. **Initial Setup (Workshop)**: Use NFC to configure Modbus address, baud rate, parity (unpowered mode)
2. **Site Installation**: Wire RS485 network, verify Modbus communication with BMS/SCADA
3. **Remote Monitoring**: BMS/SCADA continuously polls TK4 MB via Modbus (valve status, alarms, cycle count)
4. **Field Adjustments (NFC)**: Technician uses NFC to fine-tune valve timings without interrupting Modbus communication
5. **Alarm Response**: BMS detects alarm via Modbus register 40002 → Technician uses NFC diagnostics to identify cause → Clear alarm via NFC or Modbus write

**Advantages of Dual Communication:**
- **Centralized Monitoring (Modbus)**: System-wide visibility, historical logging, automated alarm responses
- **Local Configuration (NFC)**: Fast on-site adjustments, no need for BMS reconfiguration
- **Redundancy**: If Modbus network down, NFC still allows local diagnostics and configuration
- **Flexibility**: Choose optimal interface for task (remote monitoring vs. local setup)

**Use Case Example - Supermarket Refrigeration (20 TK4 MB Units):**
- **Modbus Network**: All 20 units wired to central BMS in backroom → BMS displays oil levels, alarms on HMI
- **NFC Configuration**: Technician walks through equipment areas with handheld Android tablet + dongle → Adjusts cycle timings on individual units → No need to access BMS or open electrical panels
- **Result**: System integrator manages global monitoring (BMS/Modbus), field technician handles local optimization (NFC), both work simultaneously without interference

---

### 10.4 Advanced Modbus Features (Via NFC Configuration)

**Modbus Response Time Optimization:**
- **Parameter**: Response delay (0-250ms)
- **Default**: 10ms (safe for most systems)
- **Slow BMS/PLC**: Increase to 50-100ms if master reports timeout errors
- **Fast BMS/PLC**: Decrease to 0-5ms for faster polling cycles

**Broadcast Commands (Address 0):**
- **Function**: Master sends write command to address 0 → All TK4 MB units execute command simultaneously
- **Use Case**: Reset cycle counter on all units at once (maintenance synchronization)
- **Limitation**: No response from slaves (write-only, cannot read)

**Modbus Exception Responses:**
- TK4 MB returns exception codes for invalid requests:
  - **Exception 01**: Illegal function (unsupported function code)
  - **Exception 02**: Illegal data address (register does not exist)
  - **Exception 03**: Illegal data value (write value out of range)

**Register Update Rate:**
- **Real-Time Registers** (40001-40005): Updated every 100ms (valve status, oil level, alarms)
- **Diagnostic Registers** (40006-40009): Updated every 1 second (cycle counter, power-on time)
- **Polling Recommendation**: Poll critical registers (40001-40005) every 1-5 seconds, diagnostics (40006-40009) every 30-60 seconds

---

### 10.5 Comparison: Modbus RTU vs. NFC Nano Interface

| Feature | Modbus RTU (RS485) | NFC Nano Interface |
|---------|--------------------|--------------------|
| **Purpose** | Remote monitoring & control | Local configuration & diagnostics |
| **Range** | Up to 1200m per segment | 5-10 cm proximity |
| **Connection** | Wired (twisted pair cable) | Wireless (through plastic enclosures) |
| **Continuous Communication** | Yes (real-time polling) | No (session-based) |
| **Device Required** | BMS/SCADA/PLC (user-provided) | TK4-PRG-NANO dongle (€100-150) |
| **Multi-Unit Monitoring** | Yes (32 units per segment) | No (one unit at a time) |
| **Configuration Access** | Limited (via BMS software) | Full (dedicated app) |
| **Real-Time Monitoring** | Yes (valve status, alarms) | Yes (powered mode only) |
| **Historical Data** | Yes (BMS logging) | No (read current values only) |
| **Alarm Integration** | Yes (BMS alarm system) | No (local diagnostics only) |
| **Use Case** | System-wide monitoring | Commissioning, troubleshooting, optimization |
| **Best For** | Centralized control, SCADA/BMS integration | Field service, local adjustments, pre-configuration |

**Recommendation**: Use **both interfaces** for complete lifecycle management:
- **Modbus RTU**: Continuous monitoring, alarm integration, historical logging (system integrator responsibility)
- **NFC**: Commissioning, fine-tuning, troubleshooting, maintenance (field technician responsibility)

---

### 10.6 Troubleshooting Connectivity Issues

#### Modbus RTU Issues

**Symptom: BMS cannot communicate with TK4 MB**
- **Check 1**: Verify RS485 wiring (A/B not reversed, 120Ω termination at both ends)
- **Check 2**: Confirm slave address matches BMS configuration (use NFC to read address from TK4 MB)
- **Check 3**: Verify baud rate/parity match (TK4 MB default: 9600 bps Even parity, check BMS settings)
- **Check 4**: Test with single TK4 MB unit (disconnect others, isolate faulty device)
- **Check 5**: Use Modbus diagnostic tool (USB-to-RS485 adapter + Modbus poll software on PC)

**Symptom: Intermittent communication (frequent timeouts)**
- **Check 1**: Measure cable resistance (should be <5Ω per 100m)
- **Check 2**: Check for EMI sources (VFDs, motors, high-voltage cables parallel to RS485)
- **Check 3**: Verify termination resistors (measure 60Ω between A/B at both ends)
- **Check 4**: Increase response delay (use NFC to set TK4 MB response delay to 50-100ms)

**Symptom: One device not responding (others OK)**
- **Check 1**: Verify unique slave address (duplicate address causes conflicts)
- **Check 2**: Use NFC to read configuration (check address, baud rate, parity)
- **Check 3**: Test device isolation (temporarily change address to unused value, re-test)

#### NFC Issues

**Symptom: Dongle not detected by PC/Android**
- **Check 1**: Verify USB cable connected (blue LED on dongle should illuminate)
- **Check 2**: Try different USB port (some PCs disable USB ports in power-saving mode)
- **Check 3**: Install USB drivers (Windows may require driver installation on first use)
- **Check 4**: Check Android OTG support (enable "USB OTG" in Android settings)

**Symptom: TK4 MB not detected by dongle**
- **Check 1**: Position dongle flat against TK4 MB body (near label, 5-10 cm proximity)
- **Check 2**: Remove metal obstructions (NFC does not penetrate metal enclosures)
- **Check 3**: Check plastic thickness (effective through <5mm, thicker enclosures reduce range)
- **Check 4**: Verify TK4 MB NFC antenna intact (physical damage rare, inspect if dropped)

**Symptom: Cannot write parameters (read-only access)**
- **Check 1**: Password protection enabled? (enter password in app to unlock write access)
- **Check 2**: Powered mode required? (some parameters need TK4 MB energized)
- **Check 3**: App permission issue (Android: grant USB access permission in system settings)

---

## Document Information

**Document**: TK4 MB Series Complete Product Documentation  
**Version**: 2.0  
**Date**: 2025-11-15  
**Language**: English  
**Product Family**: TK4 MB Smart Oil Level Regulators (46/80/130 bar) with Modbus RTU + NFC Dual Connectivity  
**Category**: Oil_Level_Regulators  
**Keywords**: TK4 MB, smart oil level regulator, Modbus RTU, RS485 serial, NFC Nano Interface, dual communication, BMS integration, SCADA, TK4-PRG-NANO, wireless configuration, remote monitoring, 46 bar, 80 bar, 130 bar, CO2 subcritical, CO2 transcritical

**© 2025 Teklab. All rights reserved.**
