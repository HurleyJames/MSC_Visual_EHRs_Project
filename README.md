<p align="center">
    <img width="400" src="./assets/EHRs.jpg">
</p>


<div align="center">
    <span><a target="_blank" href="README-zh.md">🇨🇳 中文文档</a></span>
    <span>|</span>
    <span>🇬🇧 English Version</span>
</div>

<div align="center">
    <strong>A visual data profiling tool for Electronic Health Records (EHRs) dataset.</strong>
</div>

---

## 👀 Background

> Electronic health record (EHR) datasets often contain millions of records and involve variable that can have tens of thousands of different codes. Data mining techniques for profiling data are well-developed and available in a toolkits such as Pandas, but only use basic visualizations (histograms, scatterplots, etc) to help analysts understand data profiles. Leading commercial visualization tools (e.g., Tableau) are primarily designed to allow users to gain high-level overviews, and to drill down and explore data. That supports basic types of profiling, but not the complexity of data such as electronic health records (EHRs) which are characterised by noisy longitudinal sequences of events (diagnoses, procedures, prescriptions, etc.).

## 🎯 Aim

The aim of this project is to investigate effective visualization techniques for profiling EHRs, and implement them in a Python tool. Hence, this project will develop compact (sparkline-type or based on glyphs) methods that allow users to visualize descriptive statistics for hundreds of variables at a time. The descriptive statistics (see Abedjan et al., 2015) include cardinalities (e.g., null values and uniqueness), distributions (e.g., whole value and first digit), patterns (e.g., formats and character sets), and comparisons of pairs of fields (e.g., admission vs. discharge date). The tool will allow users to interactively sort and filter the data that is displayed, perform simple aggregations (e.g., to combine fields or profile the first N characters of an EHR code) and simultaneously show visual profles for multiple subsets of the data (e.g., different years).

## 🚀 Quick start

1. Open this Django project by Pycharm and type `python manage.py runserver` in the terminal.
2. Enter `localhost:8080/datagrid` in the browser, upload the `test_data.csv` file in the `EHR_statistic_app` directory of this project, select `Program_Year` or `Payment_Year` in the top bar `Provider Name`, and then click the `Submit` button to see the visual analysis interface.

## 🖥 Screenshot

![](./assets/screenshot.png)

## 📝 Reference

* Abedjan, Z., Golab, L., & Naumann, F. (2015). Profiling relational data: a survey. The VLDB Journal, 24(4), 557-581.
* Ruddle, R. A., & Hall, M. S. (2019). Using miniature visualizations of descriptive statistics to investigate the quality of electronic health records. Proceedings of the International Conference on Health Informatics (HEALTHINF). https://raruddle.files.wordpress.com/2019/01/ruddle-healthinf-2019.pdf