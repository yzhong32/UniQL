#!/bin/bash

# 设置SQLite数据库所在的目录
DIRECTORY=~/spider/database

# 设置日志文件的路径
FAIL_LOG_FILE=~/migration_failures.log
SUCCESS_LOG_FILE=~/migration_success.log

# MySQL数据库的用户名和密码
MYSQL_USER=cs511
MYSQL_PASSWORD=cs511password

DB_FILES=("$DIRECTORY"/*/*.sqlite)

# 初始化计数器
cur_offset=0
offset=0
cur_count=0
total=${#DB_FILES[@]}

echo "total file num: ${total}"

if [ -f "offset.txt" ]; then
  offset=$(cat offset.txt)
  cur_offset=$offset
fi

echo "current offset: ${offset}"c

# 迁移每个SQLite数据库，但限制为10个
for sqlite_file in "${DB_FILES[@]}"; do
  # 跳过已经处理的
  if [ $offset -gt 0 ]; then 
    ((offset--))
    echo "skip ${sqlite_file}"
    continue
  fi
  # 检查是否已经完成
  if [ $cur_offset -ge $total ]; then
    echo "Migration completed"
    break 
  fi

  # 检查是否已经迁移了5个数据库
  if [ $cur_count -ge 5 ]; then
    echo "Migration limit reached (${cur_count} databases)."
    break # 终止循环
  fi

  # 获取不带路径和扩展名的数据库名
  DB_NAME=$(basename "$sqlite_file" .sqlite)
  echo "Migrate ${DB_NAME}"
  # 首先，尝试删除MySQL中已存在的同名数据库（忽略错误，可能数据库不存在）
  sudo mysql -u root  -e "DROP DATABASE IF EXISTS \`$DB_NAME\`;" 2>/dev/null
  sudo mysql -u root  -e "CREATE DATABASE ${DB_NAME};" 2>/dev/null
  # 执行迁移命令
  sudo sqlite3mysql -f "${sqlite_file}" -d "$DB_NAME" -u "$MYSQL_USER" --mysql-password "$MYSQL_PASSWORD" 2>&1

  # 检查上一个命令的退出状态
  if [ $? -ne 0 ]; then
    # 如果迁移失败，记录到日志文件
    echo "Migration failed for $DB_NAME" >> "$FAIL_LOG_FILE"
  else
    echo "Migration succeeded for $DB_NAME" >> "$SUCCESS_LOG_FILE"
  fi

  # 增加计数器
  ((cur_count++))
  ((cur_offset++))
done

echo  $cur_offset > offset.txt 

# 输出失败的迁移
if [ -s "$FAIL_LOG_FILE" ]; then
  echo "Failed migrations are logged in $FAIL_LOG_FILE"
  cat "$FAIL_LOG_FILE"
else
  echo "No migration failures."
fi

echo "----------------||||||||||||success|||||||||||||------------------"
cat "$SUCCESS_LOG_FILE"