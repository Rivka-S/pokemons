
use mysql;
select * from type_of_poke;
drop table type_of_poke;
drop table pokemon_ownes_by;
drop table pokemons;
drop table owners;


create table pokemons(
    id int primary key,
    name varchar(20),
    height int,
    weight int
);


create table type_of_poke(
    pokemon_id int,
    type_name varchar(20),
    foreign key (pokemon_id) references pokemons(id), 
    primary key (pokemon_id, type_name)
);

create table owners(
    name varchar (20) primary key,
    town varchar(20) 
);

create table pokemon_ownes_by(
    pokemon int,
    owner varchar(20),
    foreign key (pokemon) references pokemons(id),
    foreign key (owner) references owners(name),
    primary key (pokemon, owner)
);