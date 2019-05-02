git checkout develop

git pull
databricks workspace export_dir -o /Users/pete@tamisin.com/Demo ./Workspace

dt=`date '+%Y-%m-%d %H:%M:%S'`
msg_default="DB export on $dt"
read -p "Enter the commit comment [$msg_default]: " msg
msg=${msg:-$msg_default}
echo $msg

git add .
git commit -m "$msg"
git push
