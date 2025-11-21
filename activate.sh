start() {
	source dungeon_env/bin/activate
	export PYTHONPATH="$PYTHONPATH:$(pwd)"
	python3 src/app.py
}

clean() {
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf */*/*/__pycache__
}

launch() {
	clean
	python3 src/app.py
}

case "$1" in
  start)
    start
    ;;
  clean)
    clean
    ;;
  launch)
	launch
	;;
  help)
	echo "Accessible commands: start | launch | clean | help"
	;;
  *)
    echo "Unknown command: $1"
    echo "Accessible commands: start | launch | clean | help"
    exit 1
    ;;
esac