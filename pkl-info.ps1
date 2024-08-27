
# ------------------------------------------------------------------------------
function get-disk-usage ([string[]]$dirs)
{
    foreach ($dir in $dirs)
    {
        [pscustomobject]@{
            'Directory' = $dir
            'Size' = (Get-ChildItem $dir -Recurse | Measure-Object -Property Length -Sum).Sum
        }
    }
}

function get-disk-usage-formatted ([string[]]$dirs)
{
    get-disk-usage $dirs | 
        Format-Table @{ Label='Directory'; Expression={$_.Directory} }, @{ Label='Size'; Expression={'{0:N0}' -f $_.Size} }
}
# ------------------------------------------------------------------------------

Write-Host 'Number of files in pkl directory:'

(Get-ChildItem .\pkl).Length

write-host 'Disk usage of pkl directory:'

get-disk-usage-formatted .\pkl

write-host 'Top 10 largest files in pkl directory:'

Get-ChildItem .\pkl | Sort-Object -Property Length -Descending | Select-Object -First 10
# ------------------------------------------------------------------------------