python_bin="$1"
python_bin="${python_bin:=python}"
echo "with python: [$python_bin]"

# package
"$python_bin" setup.py clean --all
"$python_bin" setup.py sdist bdist_wheel
if [ $? -ne 0 ] ; then
	echo "Error: package failed!"
	exit 1
fi

# upload
echo
echo "### start to upload package ###"
python3 -m twine upload dist/*

