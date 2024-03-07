use livros ;

# Análise básica ==============================================

select * from books ;
select * from ratings ;
select * from users ;

# Criar índices  ==============================================

# Índices
create index idx_books_isbn on books (isbn);
create index idx_ratings_isbn on ratings (isbn);

# Análise =====================================================

select count(*) from users where age = "" ;
# Temos uma grande quantidade idade de usuários vazia,
# Devemos considerar se utilizamos ou não

select count(*) from users where age != "" ;
# Quantidade de valores de idade preenchidos (não verificados como numérico)

select count(*) from books where isbn = 0 ;
# Livros com o ISBN vazio, não serão úteis pois não podemos relacionar eles

select ct from (select count(*) as ct, isbn from books group by isbn) as isbns where ct > 1 or ct = 0 ;
# Verificar se há inconsistências no ISBN (valores repetidos)

select count(*), Year_Of_Publication from books group by Year_Of_Publication ;
# Anos inválidos

# Dropar colunas não utilizadas ================================

# Usuários
alter table users drop `Location` ;

# Livros
alter table books drop `Image_URL` ;
alter table books drop `Book_Title` ; # O ISBN Já faz o trabalho de identificar o livro

# Renomear colunas =============================================

alter table books rename column `Book_Author` to `autor` ;
alter table books rename column `Publisher` to `editora` ;
alter table books rename column `Year_Of_Publication` to `ano` ;

alter table ratings rename column `Book_Rating` to `nota` ;

alter table users rename column `Age` to `idade` ;

# Deletar dados ===============================================

set SQL_SAFE_UPDATES = 0;

# Livros com isbn inválidos
delete from books where isbn in (select isbn from (select count(*) as ct, isbn from books group by isbn) as isbns where ct > 1 or ct = 0);

# Livros com ano de publicação inválidos
delete from books where `ano` = 0 ;

# Avaliações sem livros relacionados
delete from ratings where isbn not in (select isbn from books);

set SQL_SAFE_UPDATES = 1;

# Joins ========================================================

# Chaves primárias e estrangeiras
alter table books add primary key (isbn);
alter table ratings add foreign key (isbn) references books(isbn) ;

select 
	b.isbn,
    autor,
    ano,
    editora,
    user_id,
    nota
from books b join ratings r 
on b.isbn = r.isbn ;
