row_str = ""
            for tile in range(len(row)):
                row_str += row[tile] if row[tile] in self.tiles.keys() \
                    else EMPTY
                print(row_str)


return '\n'.join(self.id_list)

str_row = ''
        for row in self.maze_rows:
            str_id = ''
            for tile in row:
                str_id += tile.get_id()
            str_row += (str_id + '\n')
        return str(str_row[0:-1])


'D LL#\n##D##\n#   #\n#####\nD LL#\n#####' !=
'#####\nD LL#\n#####
