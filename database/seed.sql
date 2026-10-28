USE [NarraDB];
GO

IF NOT EXISTS (
    SELECT 1 FROM dbo.[Типы материалов]
    WHERE [Наименование материала] = N'Музыка'
)
    INSERT INTO dbo.[Типы материалов] ([Наименование материала])
    VALUES (N'Музыка');
GO

IF NOT EXISTS (
    SELECT 1 FROM dbo.[Типы материалов]
    WHERE [Наименование материала] = N'Фильм'
)
    INSERT INTO dbo.[Типы материалов] ([Наименование материала])
    VALUES (N'Фильм');
GO

IF NOT EXISTS (
    SELECT 1 FROM dbo.[Типы материалов]
    WHERE [Наименование материала] = N'Сериал'
)
    INSERT INTO dbo.[Типы материалов] ([Наименование материала])
    VALUES (N'Сериал');
GO

IF NOT EXISTS (
    SELECT 1 FROM dbo.[Типы материалов]
    WHERE [Наименование материала] = N'Книга'
)
    INSERT INTO dbo.[Типы материалов] ([Наименование материала])
    VALUES (N'Книга');
GO

IF NOT EXISTS (
    SELECT 1 FROM dbo.[Типы материалов]
    WHERE [Наименование материала] = N'Игра'
)
    INSERT INTO dbo.[Типы материалов] ([Наименование материала])
    VALUES (N'Игра');
GO