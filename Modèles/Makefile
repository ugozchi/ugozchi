# Variables
NAME = libft.a
CC = cc
CFLAGS = -Wall -Werror -Wextra -g3
RM = rm -rf
AR = ar rcs

# Colors (When you change colors or styles using echo, you need to RESET the parameters at the end of the sentence.)
RESET	=	\033[0m
BLACK	=	\033[0;30m
RED	=	\033[0;31m
GREEN	=	\033[1;32m
YELLOW	=	\033[1;33m
BLUE	=	\033[0;34m
PURPLE	=	\033[1;35m
CYAN	=	\033[1;36m
WHITE	=	\033[0;37m

# Styles (To change a style, you have to change the "0" after the open square bracket "[" in "Colors" to the following numbers.)
# NORMAL = 0
# BOLD = 1
# LOW INTENSITY = 2
# ITALIC = 3
# UNDERLINED = 4
# BLINKING = 5
# INVERTED/UNDERLINE = 7
# HIDDEN = 8
# CROSSED OUT = 9 

# Symbols
OK	=	✓
FAIL	=	✗
INFO	=	ⓘ

# Sources and Objects
SRCS		=	ft_exemple1.c \
				ft_exemple2.c \
				ft_exemple3.c \
				ft_exemple4.c \
				ft_exemple5.c \


SRC_COUNT	=	${words ${SRCS}}

OBJS		=	$(addprefix ${OBJ_DIR}/, $(notdir $(SRCS:.c=.o)))
OBJ_DIR		=	.o

all:			${OBJ_DIR} ${NAME}

${NAME}:		entry_message ${OBJS}
				@if [ -e ${NAME} ] && [ "$(shell find ${OBJ_DIR} -newer ${NAME} 2>/dev/null)" = "" ]; then \
					echo "${YELLOW}${INFO} Nothing to do !${RESET}"; \
				else \
					echo "${GREEN} DONE${RESET}"; \
					${AR} ${NAME} ${OBJS} && echo "${CYAN}Creating ${NAME} archive file${RESET}"; \
					echo "${PURPLE}${NAME} created${RESET}"; \
				fi

${OBJ_DIR}:
				@if [ ! -d "${OBJ_DIR}" ]; \
				then mkdir -p "${OBJ_DIR}"; \
				fi

${OBJ_DIR}/%.o: %.c
				@printf "${GREEN}"
				@printf "%s" "${OK}"
				@printf "${NC}"
				@${CC} ${CFLAGS} -c $< -o $@

# so: is here for the libft-unit-test
so:
	${CC} -nostartfiles -fPIC ${CFLAGS} ${SRCS}
	gcc -nostartfiles -shared -o libft.so ${OBJS}
        
clean:
			@if [ ! -d "${OBJ_DIR}" ]; \
			then \
				echo "${YELLOW}${INFO} Repo .o already clean${RESET}"; \
			else \
				echo "${RED}Removing all .o files${RESET}"; \
				${RM} ${OBJ_DIR}; \
			fi

fclean:			clean
			@if [ ! -f "${NAME}" ]; \
			then \
				echo "${YELLOW}${INFO} Archive file already clean${RESET}"; \
			else \
				echo "${RED}Removing archive files${RESET}"; \
				${RM} ${NAME}; \
			fi

re:				fclean all

entry_message:
				@echo "${YELLOW}${INFO} ${SRC_COUNT} files of the library:\n${GREEN}Compilation :${RESET}"

.PHONY:			all clean fclean re entry_message
