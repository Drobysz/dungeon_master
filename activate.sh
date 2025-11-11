start() {
	source dungeon_env/bin/activate
	export PYTHONPATH="$PYTHONPATH:$(pwd)"
	python3 main.py
}

clean() {
	if [ ! -z "$(ls -A "imgs")" ]; then
		rm imgs/*
	fi
}

launch() {
	clean
	python3 main.py
}

reset() {
	
}

delete() {
	clean
	rm -rf tp2_env
	rm -rf helpers/__pycache__
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
  reset)
    reset
    ;;
  delete)
    delete
    ;;
  help)
	echo "Accessible commands: start | launch | clean | reset | delete | help"
	;;
  *)
    echo "Unknown command: $1"
    echo "Accessible commands: start | launch | clean | reset | delete | help"
    exit 1
    ;;
esac