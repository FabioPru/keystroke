#sample usage ./iterate_JSON node hello

echo "Iterating the command:" "$@"


for sem in ../../pads/*; do
    echo "inspecting $sem"
    for user in "$sem"/*; do
        echo "    inspecting $user"
        for filename in "$user"/*.json; do
            echo "        Acting on " "$filename"
            "$@" "$filename"
        done
    done
done
