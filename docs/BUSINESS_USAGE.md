# Business Usage & Workflows

## 1. Executive Overview
The **StatsApp** (internally known as Trimagos / Sigmaway platform) is a comprehensive Statistical, Quality Management, and Data Analytics platform. It is designed to help quality engineers, data analysts, and project managers streamline Six Sigma methodologies, track project health, and run advanced inferential/predictive analytics without writing code.

The platform provides an end-to-end web interface for:
- Data ingestion and normalization.
- Process mapping and defect tracking.
- Descriptive and Inferential Statistics.
- Quality Tools (FMEA, Opportunity Trackers).
- Machine Learning (Linear and Multiple Regression).

## 2. Core Modules & Features

### A. Datasets (`apps/datasets`)
*Formerly `upload`*
- **Purpose**: The foundation of the platform. Users upload `.csv` or `.xlsx` files which are ingested into the database.
- **Features**: 
  - File upload with automatic CSV parsing (`PapaParse`).
  - Column metadata management (identifying Data Types: Numeric, Categorical).
  - Deleting and managing existing datasets.

### B. Processes (`apps/processes`)
*Formerly `process`*
- **Purpose**: Represents a project or a business process being analyzed (e.g., "Manufacturing Line A Defect Rate").
- **Features**:
  - Linking datasets to a specific Process.
  - Tracking process lifecycle.

### C. Analytics (`apps/analytics`)
*Formerly `statistical` and `charts`*
- **Purpose**: Core engine for generating insights from datasets.
- **Features**:
  - **Descriptive Statistics**: Mean, median, standard deviation, variance.
  - **Hypothesis Testing**: T-Tests, ANOVA, Chi-Square.
  - **Data Visualization**: Dynamic generation of charts (Bar, Line, Scatter, Control Charts) based on selected Dataset dimensions and measures.

### D. Machine Learning (`apps/machinelearning`)
*Formerly `mlearn`*
- **Purpose**: Predictive modeling based on historical data.
- **Features**:
  - **Linear Regression**: Simple modeling between one dependent and one independent variable.
  - **Multiple Regression**: Complex models utilizing multiple predictors.

### E. Quality Tools (`apps/qualitytools`)
*Formerly `qtools`*
- **Purpose**: Standard Six Sigma and Quality Assurance templates.
- **Features**:
  - **FMEA** (Failure Mode and Effects Analysis): Documenting potential failures, severity, occurrence, and detection ratings.
  - **Opportunity Tracker**: Logging improvement opportunities and tracking their implementation.

### F. Process Mapping (`apps/processmap`)
- **Purpose**: Visualizing workflows.
- **Features**:
  - Interactive flowchart builder.
  - Saving and loading process maps.

## 3. Typical User Journey
1. **Authentication**: User signs up and is approved by an administrator, or logs in with existing credentials.
2. **Data Ingestion**: User navigates to `Datasets` -> `Upload` and drops a CSV file. The system parses the file and creates a new `Dataset` record.
3. **Process Creation**: User creates a new `Process` and attaches the uploaded Dataset to it.
4. **Exploratory Analysis**: User opens `Analytics` -> `Charts` to visualize trends, and uses `Statistical` to run descriptive stats on key columns.
5. **Quality Tracking**: If defects are found, the user logs them in `Quality Tools` -> `FMEA`.
6. **Predictive Modeling**: User builds a Regression model in `Machine Learning` to predict future defects based on independent variables.
