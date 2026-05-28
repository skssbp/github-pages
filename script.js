const subnm = {

    '301': 'ENG',
    '042': 'PHY',
    '043': 'CHEM',
    '044': 'BIO',
    '048': 'PHE',
    '835': 'MMS',
    '041': 'MTH',
    '049': 'PAINT',
    '083': 'COMP',
    '030': 'ECO',
    '054': 'BST',
    '055': 'ACCT',
    '811': 'BNK',
    '028': 'POLSC',
    '029': 'GEO',
    '039': 'SOCIO',
    '027': 'HIST',
    '034': 'MUSIC',
    '302': 'HINDI-C'
};

function convertFile() {

    const fileInput = document.getElementById('fileInput');

    const file = fileInput.files[0];

    if (!file) {

        alert("Please select a TXT file");

        return;
    }

    const reader = new FileReader();

    reader.onload = function(e) {

        const text = e.target.result;

        processText(text);
    };

    reader.readAsText(file);
}

function processText(text) {

    const lines = text.split('\n');

    let csvData = [];

    let headers = [
        'RN',
        'NAME',
        'ENG',
        'PHY',
        'CHEM',
        'BIO',
        'MTH',
        'COMP',
        'TOT',
        'PER',
        'RESULT'
    ];

    csvData.push(headers);

    for (let i = 0; i < lines.length; i++) {

        let b = lines[i].trim().split(/\s+/);

        if (b.length > 0 &&
            !isNaN(b[0]) &&
            parseInt(b[0]) >= 100) {

            let row = {};

            row['RN'] = b[0];

            if (b.includes('301')) {

                row['NAME'] = b.slice(
                    2,
                    b.indexOf('301')
                ).join(' ');

                let subjects = b.slice(
                    b.indexOf('301')
                );

                i++;

                let marksLine = lines[i]
                    .trim()
                    .split(/\s+/);

                let marks = marksLine.filter(
                    x => !isNaN(x)
                );

                let total = 0;

                for (let j = 0; j < marks.length; j++) {

                    total += parseInt(marks[j]);

                    if (subjects[j] in subnm) {

                        row[subnm[subjects[j]]] = marks[j];
                    }
                }

                row['TOT'] = total;

                row['PER'] = (
                    total / marks.length
                ).toFixed(2);

                row['RESULT'] = subjects[
                    subjects.length - 1
                ];

                let csvRow = headers.map(
                    h => row[h] || ''
                );

                csvData.push(csvRow);
            }
        }
    }

    downloadCSV(csvData);
}

function downloadCSV(data) {

    let csvContent = data
        .map(e => e.join(","))
        .join("\n");

    const blob = new Blob(
        [csvContent],
        { type: 'text/csv' }
    );

    const url = URL.createObjectURL(blob);

    const link = document.getElementById(
        'downloadLink'
    );

    link.href = url;

    link.download = "xiiall.csv";

    link.style.display = "block";

    link.innerText = "Download CSV";
}