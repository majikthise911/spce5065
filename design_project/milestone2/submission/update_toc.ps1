# Populate the Word TOC field in the built docx.
#
# Why this exists. Pandoc writes the TOC as a field marked w:dirty="true", and
# build_docx.py adds <w:updateFields w:val="true"/> so Word refreshes it on open.
# That still leaves the *delivered file* holding placeholder text, so anything
# that is not Word (a markdown preview, a docx viewer, Google Docs, a grader who
# clicks straight through) shows no table of contents at all.
#
# This drives Word once at build time to compute the entries and page numbers and
# bake them into the file, so the TOC is real content rather than an instruction
# to the reader.

param(
    [string]$Path = "$PSScriptRoot\Clayton_spce5065_ms2_submission.docx"
)

if (-not (Test-Path $Path)) { throw "not found: $Path" }
$Path = (Resolve-Path $Path).Path

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($Path, $false, $false)

    $doc.Repaginate()
    if ($doc.TablesOfContents.Count -gt 0) {
        $doc.TablesOfContents.Item(1).Update()
    }
    $doc.Fields.Update() | Out-Null
    $doc.Repaginate()

    Write-Output ("tables of contents : " + $doc.TablesOfContents.Count)
    Write-Output ("pages              : " + $doc.ComputeStatistics(2))
    Write-Output ("words              : " + $doc.ComputeStatistics(0))

    if ($doc.TablesOfContents.Count -gt 0) {
        $t = $doc.TablesOfContents.Item(1).Range.Text
        $lines = ($t -split "`r") | Where-Object { $_.Trim().Length -gt 0 }
        Write-Output ""
        Write-Output "--- TOC entries as Word built them ---"
        foreach ($l in $lines) { Write-Output ("  " + ($l -replace "`t", "  ...  ").Trim()) }
    }

    $doc.Save()
    $doc.Close(0)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}

Write-Output ""
Write-Output "TOC populated and saved into $Path"
